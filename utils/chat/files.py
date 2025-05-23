import os
import logging
from dotenv import load_dotenv
from openai import AsyncOpenAI
from fastapi import HTTPException, Depends
from sqlmodel import select, Session
from utils.core.db import engine
from utils.chat.models import Document

load_dotenv(override=True)

logger = logging.getLogger("uvicorn.error")

S3_BUCKET = os.getenv("S3_BUCKET")

# Helper function to get or create a vector store
async def get_vector_store(assistantId: str, client: AsyncOpenAI = Depends(lambda: AsyncOpenAI())) -> str:
    assistant = await client.beta.assistants.retrieve(assistantId)
    if assistant.tool_resources and assistant.tool_resources.file_search and assistant.tool_resources.file_search.vector_store_ids:
        return assistant.tool_resources.file_search.vector_store_ids[0]
    raise HTTPException(status_code=404, detail="Vector store not found")


# Helper function to generate the FILE_PATHS dictionary (not for production use)
def get_file_paths() -> dict[str, str]:
    with Session(engine) as session:
        documents = session.exec(select(Document)).all()
        document_dict = {doc.id: doc.storage_url for doc in documents if doc.storage_url}
        return document_dict


def cleanup_temp_file(file_path: str):
    """Removes the temporary file."""
    try:
        os.unlink(file_path)
        logger.info(f"Successfully cleaned up temporary file: {file_path}")
    except OSError as e:
        logger.error(f"Error cleaning up temporary file {file_path}: {e}")


FILE_PATHS = {
    "dl_001": "https://openknowledge.worldbank.org/bitstreams/3badf232-532e-4522-baed-f37423aecde8/download",
    "dl_003": "https://openknowledge.worldbank.org/bitstreams/051336f3-571d-4b26-9409-e18a0ac5aff5/download",
    "dl_004": "https://openknowledge.worldbank.org/bitstreams/e4fc5aed-53fe-4800-9c4f-ce6a32984da7/download",
    "dl_005": "https://openknowledge.worldbank.org/bitstreams/430dad35-ac8d-4e7e-b1cd-85266ec631ba/download",
    "dl_006": "https://openknowledge.worldbank.org/bitstreams/13f2b5c7-c196-4a10-af8d-f23d8bec663c/download",
    "dl_007": "https://openknowledge.worldbank.org/bitstreams/e3a4f7b6-247e-4a0a-bf65-68e185b3601b/download",
    "dl_008": "https://openknowledge.worldbank.org/bitstreams/45f4c808-a757-4d01-9aef-b9a4f37d6c7c/download",
    "dl_009": "https://openknowledge.worldbank.org/bitstreams/772e3d6c-7c59-4ad6-a8bb-cae218d1ce86/download",
    "dl_010": "https://openknowledge.worldbank.org/bitstreams/3da2a686-9139-4b92-81a4-3c76aaf189d5/download",
    "dl_011": "https://openknowledge.worldbank.org/bitstreams/ae5439a1-5a9f-4d45-903c-9d1678810b4c/download",
    "dl_012": "https://openknowledge.worldbank.org/bitstreams/ea1a2330-27ce-4c99-9a49-7749f9b2eaad/download",
    "dl_013": "https://openknowledge.worldbank.org/bitstreams/3d70b099-6872-40ed-9005-27efdee42967/download",
    "dl_014": "https://openknowledge.worldbank.org/bitstreams/edbfd6a9-e948-45b6-a690-18e6a12820e0/download",
    "dl_015": "https://openknowledge.worldbank.org/bitstreams/268abc8d-8e0e-437b-9615-3fe8aa395693/download",
    "dl_016": "https://openknowledge.worldbank.org/bitstreams/4f851760-bbb2-4c0c-8f4e-6855a2b9a586/download",
    "dl_017": "https://openknowledge.worldbank.org/bitstreams/41034941-5448-4df9-bfb8-6f93f32e7c4b/download",
    "dl_018": "https://openknowledge.worldbank.org/bitstreams/a0f739f1-a293-4c13-9071-a196fba9c4c5/download",
    "dl_019": "https://openknowledge.worldbank.org/bitstreams/05d9f6bd-937f-4993-8c76-4ef8f1839ab1/download",
    "dl_020": "https://openknowledge.worldbank.org/bitstreams/2318eadf-bf03-472f-b53c-4347354479b6/download",
    "dl_021": "https://openknowledge.worldbank.org/bitstreams/9d9b6887-31a0-4692-bf08-e3425266e59f/download",
    "dl_022": "https://openknowledge.worldbank.org/bitstreams/f52f748d-e94d-4b7e-a35d-bdc41b7b04a1/download",
    "dl_023": "https://openknowledge.worldbank.org/bitstreams/b60571cc-dca5-4a55-8e93-bb7d3f163a93/download",
    "dl_024": "https://openknowledge.worldbank.org/bitstreams/2bd9ba95-01e8-4492-8977-ab1a9ca8f251/download",
    "dl_025": "https://openknowledge.worldbank.org/bitstreams/df8bb927-ef7b-4649-9f0f-c3670542f974/download",
    "dl_026": "https://openknowledge.worldbank.org/bitstreams/a4331e35-4b26-439e-b4c2-ca8f8e338276/download",
    "dl_027": "https://openknowledge.worldbank.org/bitstreams/f3cc9b1b-efe9-4bda-8e1c-99a27ab7f6b9/download",
    "dl_028": "https://openknowledge.worldbank.org/bitstreams/dda3d4e7-9a54-4b88-880e-72e8ebecc2e5/download",
    "dl_029": "https://openknowledge.worldbank.org/bitstreams/ae7a6ab5-a562-4024-8a14-720b8e6fca6b/download",
    "dl_030": "https://openknowledge.worldbank.org/bitstreams/6def6eed-84ad-4762-b875-d1748ee67ad0/download",
    "dl_031": "https://openknowledge.worldbank.org/bitstreams/e79862cd-f9ea-44b9-89fd-7572f6b52a2f/download",
    "dl_032": "https://openknowledge.worldbank.org/bitstreams/317a9ea4-0ce1-4fee-ab6d-bb42fd5d7d06/download",
    "dl_033": "https://openknowledge.worldbank.org/bitstreams/9ba2cd09-5701-48fc-a634-6ab8b8245551/download",
    "dl_034": "https://openknowledge.worldbank.org/bitstreams/3d808a7c-fed7-4552-963e-1d1933892d26/download",
    "dl_035": "https://openknowledge.worldbank.org/bitstreams/18191092-31bc-47c0-b3cf-fa5782ed9690/download",
    "dl_036": "https://openknowledge.worldbank.org/bitstreams/0f4396f1-0c36-46c6-99c9-3d6de1279bbb/download",
    "dl_037": "https://openknowledge.worldbank.org/bitstreams/93d5837a-e59a-4d56-b2d6-6b2e87c578f5/download",
    "dl_038": "https://openknowledge.worldbank.org/bitstreams/e1553b3b-3ce6-4800-8f93-476e7c89d21b/download",
    "dl_039": "https://openknowledge.worldbank.org/bitstreams/422a5976-2a7b-4e27-8278-f854fc4f5582/download",
    "dl_040": "https://openknowledge.worldbank.org/bitstreams/1e0ab96b-71ed-486a-8d03-fcb20d563201/download",
    "dl_041": "https://openknowledge.worldbank.org/bitstreams/7d7218ff-7135-4942-99ba-e2bc1dcb81d8/download",
    "dl_042": "https://openknowledge.worldbank.org/bitstreams/c82e7d9b-6f0e-4154-b1ec-97cd786e251e/download",
    "dl_043": "https://openknowledge.worldbank.org/bitstreams/f74f2610-c7e2-4bcc-a55d-2188b788e29e/download",
    "dl_044": "https://openknowledge.worldbank.org/bitstreams/88f9916e-321b-4e21-ba65-baa601d8df96/download",
    "dl_045": "https://openknowledge.worldbank.org/bitstreams/78f5837a-2370-4ec5-b1df-95e0722d6e1d/download",
    "dl_046": "https://openknowledge.worldbank.org/bitstreams/61008cee-85d0-4abf-882f-329237d941dc/download",
    "dl_047": "https://openknowledge.worldbank.org/bitstreams/4bae3f69-a535-4f2f-8bc6-6e2259d5efc6/download",
    "dl_048": "https://openknowledge.worldbank.org/bitstreams/70854690-36cb-4072-bb18-0dc5eefc0788/download",
    "dl_049": "https://openknowledge.worldbank.org/bitstreams/c5270e44-a4ed-4013-ab16-be84a9372c9a/download",
    "dl_050": "https://openknowledge.worldbank.org/bitstreams/83d61654-5bad-4e61-9f87-0939624a8233/download",
    "dl_051": "https://openknowledge.worldbank.org/bitstreams/26e24e92-7211-457d-ab4e-ed66344a03e7/download",
    "dl_052": "https://openknowledge.worldbank.org/bitstreams/336df1f7-88ab-4b5f-b877-ab8107588d73/download",
    "dl_053": "https://openknowledge.worldbank.org/bitstreams/7ff64bf8-66ca-469f-840e-6303a1048073/download",
    "dl_054": "https://openknowledge.worldbank.org/bitstreams/34af663f-ee69-400e-8cfd-63fbeef1e49c/download",
    "dl_055": "https://openknowledge.worldbank.org/bitstreams/b350fc29-b3a7-4347-9b96-7bc63970915a/download",
    "dl_056": "https://openknowledge.worldbank.org/bitstreams/28531afa-49be-49b9-b6d6-3d4ae5f2ac67/download",
    "dl_057": "https://openknowledge.worldbank.org/bitstreams/cec17bf6-834c-46e3-9b22-fa0fbb4fa894/download",
    "dl_058": "https://openknowledge.worldbank.org/bitstreams/df366f08-cb51-4766-b97d-6fca6feede48/download",
    "dl_059": "https://openknowledge.worldbank.org/bitstreams/9acd0b61-944a-487c-8031-2453b81b5a52/download",
    "dl_060": "https://openknowledge.worldbank.org/bitstreams/37e9a398-3a81-4acd-80ea-f9d5d241e754/download",
    "dl_061": "https://openknowledge.worldbank.org/bitstreams/430b2d06-1440-4ef0-bc63-a673860fc193/download",
    "dl_062": "https://openknowledge.worldbank.org/bitstreams/367134df-c7f6-4899-ae87-fc217d523c97/download",
    "dl_063": "https://openknowledge.worldbank.org/bitstreams/ff0d23ef-4786-4c3d-9a47-520e13e677ce/download",
    "dl_064": "https://openknowledge.worldbank.org/bitstreams/6ece78fa-bed6-4514-852e-ea89777c57d6/download",
    "dl_065": "https://openknowledge.worldbank.org/bitstreams/f95ba85f-a27e-4e17-b433-d6c1a261d2aa/download",
    "dl_066": "https://openknowledge.worldbank.org/bitstreams/67c22b3f-7401-4912-bf9a-b9f30d0d7517/download",
    "dl_067": "https://openknowledge.worldbank.org/bitstreams/1ad1c704-3642-4cc5-b678-1ccc16df2e1a/download",
    "dl_068": "https://openknowledge.worldbank.org/bitstreams/17d0f4dc-b7ff-4618-b743-2087783c450c/download",
    "dl_069": "https://openknowledge.worldbank.org/bitstreams/a9c573e9-c53c-4127-84a3-1b37b795ad19/download",
    "dl_070": "https://openknowledge.worldbank.org/bitstreams/3eb5ae87-bb47-40fb-b054-597f120eb3c1/download",
    "dl_071": "https://openknowledge.worldbank.org/bitstreams/073c1e7e-4631-4e5d-b0b4-3c653fb491e6/download",
    "dl_072": "https://openknowledge.worldbank.org/bitstreams/544c538e-83f9-4775-b15e-80ff9afc9344/download",
    "dl_073": "https://openknowledge.worldbank.org/bitstreams/a7e43475-55b0-4b6c-bfb1-5c23ebad1957/download",
    "dl_074": "https://openknowledge.worldbank.org/bitstreams/47fd7cea-774e-448e-a6eb-1215aba3378b/download",
    "dl_075": "https://openknowledge.worldbank.org/bitstreams/715c3822-4a9d-437f-8b3c-89585f7fe3b0/download",
    "dl_076": "https://openknowledge.worldbank.org/bitstreams/b0b2f199-fe32-4d0e-9a33-1cba53d86462/download",
    "dl_077": "https://openknowledge.worldbank.org/bitstreams/0d3386c6-6130-4c61-a44c-7c168def6691/download",
    "dl_078": "https://openknowledge.worldbank.org/bitstreams/e5a7a596-b5c5-4805-90a1-67619c30840e/download",
    "dl_079": "https://openknowledge.worldbank.org/bitstreams/262a447e-9f65-4e9b-9e84-5f8c399b42dc/download",
    "dl_080": "https://openknowledge.worldbank.org/bitstreams/a36a3457-dfab-4239-939c-28c5d252d2dc/download",
    "dl_081": "https://openknowledge.worldbank.org/bitstreams/bbbc10c7-c684-4142-be27-c4c0cea0b75d/download",
    "dl_082": "https://openknowledge.worldbank.org/bitstreams/250be27b-0357-4b93-97ed-68c55051e4f5/download",
    "dl_083": "https://openknowledge.worldbank.org/bitstreams/89f67367-f915-4369-8f30-9afbc6d89741/download",
    "dl_084": "https://openknowledge.worldbank.org/bitstreams/e4e889f5-582f-4cbd-9394-b67a65b21cd2/download",
    "dl_085": "https://openknowledge.worldbank.org/bitstreams/c62ad0bf-1775-4cd6-845d-aaf4976de0aa/download",
    "dl_086": "https://openknowledge.worldbank.org/bitstreams/fa8c7de8-ee56-4f32-960c-b92082a22bcf/download",
    "dl_087": "https://openknowledge.worldbank.org/bitstreams/ca4b04f1-eb92-4f80-b851-6989fa6ef676/download",
    "dl_088": "https://openknowledge.worldbank.org/bitstreams/8f2474ab-d3dc-467c-b625-c000623a68c2/download",
    "dl_089": "https://openknowledge.worldbank.org/bitstreams/51f3f0c4-f0ff-4c68-b777-c364ba70dea9/download",
    "dl_090": "https://openknowledge.worldbank.org/bitstreams/fb44f7bf-242f-43fb-9c9b-d0d78900f290/download",
    "dl_091": "https://openknowledge.worldbank.org/bitstreams/eb32ecbe-ddef-42c4-b786-df22cc6c572c/download",
    "dl_092": "https://openknowledge.worldbank.org/bitstreams/dd44cbe0-ade9-4f7c-a779-4a89710ecc73/download",
    "dl_093": "https://openknowledge.worldbank.org/bitstreams/22df7ce6-859a-4602-902c-11aa9a6fb3f1/download",
    "dl_094": "https://openknowledge.worldbank.org/bitstreams/189ba2b0-435e-4e57-9e7a-64bf7cc4101f/download",
    "dl_095": "https://openknowledge.worldbank.org/bitstreams/915eb2e5-ee71-45b5-99ee-009337fca253/download",
    "dl_096": "https://openknowledge.worldbank.org/bitstreams/e6b2f828-cf6d-401f-9b22-cfd55239b917/download",
    "dl_097": "https://openknowledge.worldbank.org/bitstreams/9a5f5962-7101-4ac4-9972-00cee75fcb10/download",
    "dl_098": "https://openknowledge.worldbank.org/bitstreams/a85f766d-e26f-402d-9bbe-effddbbe70fe/download",
    "dl_099": "https://openknowledge.worldbank.org/bitstreams/7dccc340-f736-4af2-846c-03e696ed2919/download",
    "dl_100": "https://openknowledge.worldbank.org/bitstreams/41262f4b-6f00-4acf-9ad4-532a5ad375cc/download",
    "dl_101": "https://openknowledge.worldbank.org/bitstreams/97d3a673-58ff-4b25-b743-8ff7e45425a6/download",
    "dl_102": "https://openknowledge.worldbank.org/bitstreams/47f96e99-2e9a-48a2-b0fc-e8862ba478e5/download",
    "dl_103": "https://openknowledge.worldbank.org/bitstreams/da5356f5-60f2-4842-9470-29eae7d6146e/download",
    "dl_104": "https://openknowledge.worldbank.org/bitstreams/79ae5b3c-be5a-4a86-afbd-55b5cddbb11c/download",
    "dl_105": "https://openknowledge.worldbank.org/bitstreams/a5203f40-25c8-42c5-8338-7e11730e7c4e/download",
    "dl_106": "https://openknowledge.worldbank.org/bitstreams/f3707bbe-e1fc-412b-adc1-5cfc30f72672/download",
    "dl_107": "https://openknowledge.worldbank.org/bitstreams/625a4e1c-18f6-46a7-ac70-184b038dacf6/download",
    "dl_108": "https://openknowledge.worldbank.org/bitstreams/84e32dea-8cd3-4295-9258-19d9746493f7/download",
    "dl_109": "https://openknowledge.worldbank.org/bitstreams/d3107c46-82ec-41e7-9aef-2ff04abc6c3c/download",
    "dl_110": "https://openknowledge.worldbank.org/bitstreams/79b4732d-63a6-41ea-bfff-75f656a826f5/download",
    "dl_111": "https://openknowledge.worldbank.org/bitstreams/09fb7bd1-f3e4-484f-9549-fc611e0a092f/download",
    "dl_112": "https://openknowledge.worldbank.org/bitstreams/29c6ddc6-e4a0-41ab-bab6-ccdc365c77b6/download",
    "dl_113": "https://openknowledge.worldbank.org/bitstreams/394b9ab5-878b-42bd-bd19-374d05aac64e/download",
    "dl_114": "https://openknowledge.worldbank.org/bitstreams/2b36b119-67fd-4a7b-bcb5-548dd0e7d85d/download",
    "dl_115": "https://openknowledge.worldbank.org/bitstreams/9693d7f2-e4b9-45c9-ac1c-ca28146e0248/download",
    "dl_116": "https://openknowledge.worldbank.org/bitstreams/a30f00ce-77ad-4fd6-9257-d781ada53d1b/download",
    "dl_117": "https://openknowledge.worldbank.org/bitstreams/95a27a53-0577-4e31-b54b-9989ba7476e2/download",
    "dl_118": "https://openknowledge.worldbank.org/bitstreams/e130351c-4fd4-4148-af2e-aeecb47d7366/download",
    "dl_119": "https://openknowledge.worldbank.org/bitstreams/0246a6db-4ba3-4d94-bc72-0c31493bc613/download",
    "dl_120": "https://openknowledge.worldbank.org/bitstreams/db1aac1a-6e57-4563-8664-2e30b11538f8/download",
    "dl_121": "https://openknowledge.worldbank.org/bitstreams/0cd4b1e0-963a-4004-9a6f-f43919700d52/download",
    "dl_122": "https://openknowledge.worldbank.org/bitstreams/05164ea2-f134-40b7-b81e-ebfc7e45864f/download",
    "dl_123": "https://openknowledge.worldbank.org/bitstreams/db774c3e-b275-4a08-87a3-66c6116ee214/download",
    "dl_124": "https://openknowledge.worldbank.org/bitstreams/90feb71e-cdf2-476e-8299-dde20074a309/download",
    "dl_125": "https://openknowledge.worldbank.org/bitstreams/54dd7327-63cc-4d40-8ab2-8408f9573f0c/download",
    "dl_126": "https://openknowledge.worldbank.org/bitstreams/d025fec0-ff90-4d3e-b49f-f57ce74a79ad/download",
    "dl_127": "https://openknowledge.worldbank.org/bitstreams/b897242d-ab21-4933-b9c9-5c4e9ff15936/download",
    "dl_128": "https://openknowledge.worldbank.org/bitstreams/2b9fa284-479a-4f38-9cd8-b39a569b4e7b/download",
    "dl_129": "https://openknowledge.worldbank.org/bitstreams/02722265-ecc2-40cd-abab-84f2d5d3a80c/download",
    "dl_130": "https://openknowledge.worldbank.org/bitstreams/eb0982eb-8065-447a-b9e7-078aab3465c6/download",
    "dl_131": "https://openknowledge.worldbank.org/bitstreams/761f49d0-61dd-4807-bc02-af7cbf40c545/download",
    "dl_132": "https://openknowledge.worldbank.org/bitstreams/db546163-c1e0-4446-9c64-9b5225dc7313/download",
    "dl_133": "https://openknowledge.worldbank.org/bitstreams/827b8d78-466a-453e-9159-f21d0d15061e/download",
    "dl_134": "https://openknowledge.worldbank.org/bitstreams/91160c76-1202-47db-b32f-02f90902f1d2/download",
    "dl_135": "https://openknowledge.worldbank.org/bitstreams/7fd48bbe-16d9-4171-be8d-4a67b0e65271/download",
    "dl_136": "https://openknowledge.worldbank.org/bitstreams/af026935-5f2d-4edd-b19e-d8fb66f6e9da/download",
    "dl_137": "https://openknowledge.worldbank.org/bitstreams/427fb556-5355-431f-a8a1-1e0ef445687a/download",
    "dl_138": "https://openknowledge.worldbank.org/bitstreams/9c04afce-44d2-43c2-9098-1cf98722c18f/download",
    "dl_139": "https://openknowledge.worldbank.org/bitstreams/fd36997e-3890-456b-b6f0-d0cee5fc191e/download",
    "dl_140": "https://openknowledge.worldbank.org/bitstreams/8c0713d7-5768-4f2c-9be5-e5aa1a3855b5/download",
    "dl_141": "https://openknowledge.worldbank.org/bitstreams/97ed886f-3a18-4301-ba8d-998bc23d8041/download",
    "dl_142": "https://openknowledge.worldbank.org/bitstreams/b3b47f29-33a4-4a80-bc5e-3970864502e4/download",
    "dl_143": "https://openknowledge.worldbank.org/bitstreams/816ae78d-a303-4d67-b5e1-f860f958cb9f/download",
    "dl_144": "https://openknowledge.worldbank.org/bitstreams/446e1ca1-6542-4c9f-aac9-94ca426258fb/download",
    "dl_145": "https://openknowledge.worldbank.org/bitstreams/fc711754-a583-4f65-8ddd-712456e571fa/download",
    "dl_146": "https://openknowledge.worldbank.org/bitstreams/c2a8d937-5947-5320-9625-559251c55662/download",
    "dl_147": "https://openknowledge.worldbank.org/bitstreams/877259ce-4038-5741-8e78-038d27492e95/download",
    "dl_148": "https://openknowledge.worldbank.org/bitstreams/75db87a5-7b50-5006-860c-94fb0092d382/download",
    "dl_149": "https://openknowledge.worldbank.org/bitstreams/9f16ba2f-e765-4b68-aa3d-09e4c19cb17c/download",
    "dl_150": "https://openknowledge.worldbank.org/bitstreams/ecff8c4a-2c7c-4592-ac25-0fa375f8ddf5/download",
    "dl_213": "https://openknowledge.worldbank.org/bitstreams/a27f1b05-910d-59ab-ba2c-84206bf107c2/download",
    "dl_214": "https://openknowledge.worldbank.org/bitstreams/23fed1f8-6260-574a-9e2d-f4d44fb94fa3/download",
    "dl_215": "https://openknowledge.worldbank.org/bitstreams/bcadf440-bb36-5839-88c2-1d1571c8e6a2/download",
    "dl_216": "https://openknowledge.worldbank.org/bitstreams/0e81a56a-8db6-592b-a6f0-2834d974660e/download",
    "dl_217": "https://openknowledge.worldbank.org/bitstreams/d9e987cb-8b0b-51c9-baef-d2bf8e28bdd0/download",
    "dl_218": "https://openknowledge.worldbank.org/bitstreams/197f07e0-d3ec-48bc-9d52-38d551d5d312/download",
    "dl_219": "https://openknowledge.worldbank.org/bitstreams/dc86f266-37b0-5075-8ceb-6fa8fdf74562/download",
    "dl_220": "https://openknowledge.worldbank.org/bitstreams/80738fd0-5a36-41cd-ae0f-28221963db39/download",
    "dl_221": "https://openknowledge.worldbank.org/bitstreams/67932705-9dce-51f1-a073-d719b5b551f2/download",
    "dl_222": "https://openknowledge.worldbank.org/bitstreams/80bdfcf8-73b1-42b3-b107-1629f64a1f0c/download",
    "dl_223": "https://openknowledge.worldbank.org/bitstreams/bea0d1f4-be22-5d67-9e16-e3f6614c56ff/download",
    "dl_224": "https://openknowledge.worldbank.org/bitstreams/83ad0fbb-2afe-5c7b-bc0b-8409b1cbde96/download",
    "dl_225": "https://openknowledge.worldbank.org/bitstreams/a62b3bf7-6845-59a2-a70a-341121164f84/download",
    "dl_226": "https://openknowledge.worldbank.org/bitstreams/b298bc5c-6581-5713-8753-33693f71465e/download",
    "dl_151": "https://openknowledge.worldbank.org/bitstreams/f8806192-1a48-5d12-a2af-252fbf268c95/download",
    "dl_152": "https://openknowledge.worldbank.org/bitstreams/2d91534e-e769-590b-b32c-c6b9cc2363d5/download",
    "dl_153": "https://openknowledge.worldbank.org/bitstreams/c4526335-714e-5277-8f54-fd4aa83aba8c/download",
    "dl_154": "https://openknowledge.worldbank.org/bitstreams/a8aee1b8-819c-5f13-98f2-b7cbc99e6edc/download",
    "dl_155": "https://openknowledge.worldbank.org/bitstreams/149ecb3b-f261-5c8f-8e10-3b9fcd22472c/download",
    "dl_156": "https://openknowledge.worldbank.org/bitstreams/cf2a2b54-559b-5909-ada8-af36b21bd4da/download",
    "dl_157": "https://openknowledge.worldbank.org/bitstreams/c2e30f17-0d71-4590-9bec-fbc402433ef0/download",
    "dl_158": "https://openknowledge.worldbank.org/bitstreams/c60ad2be-bb9e-563b-9740-02a41f4b07dd/download",
    "dl_159": "https://openknowledge.worldbank.org/bitstreams/89c5660d-4d58-5466-83d0-e767c675614a/download",
    "dl_160": "https://openknowledge.worldbank.org/bitstreams/1ea2dd11-0471-5be6-b970-e1da55591fa0/download",
    "dl_161": "https://openknowledge.worldbank.org/bitstreams/65563763-45f9-425d-9436-caacd24b7628/download",
    "dl_162": "https://openknowledge.worldbank.org/bitstreams/b70ab1b4-6814-4b45-bf9d-b05dc01eb2a9/download",
    "dl_163": "https://openknowledge.worldbank.org/bitstreams/1d1f374f-83d6-49d5-b422-79c05533575f/download",
    "dl_164": "https://openknowledge.worldbank.org/bitstreams/2d1af64a-8d35-5946-a047-17dc143797ad/download",
    "dl_165": "https://openknowledge.worldbank.org/bitstreams/8aa74fcb-8b70-5e1f-87b9-478674c1d6b1/download",
    "dl_166": "https://openknowledge.worldbank.org/bitstreams/8ca0b138-16b0-5d33-ab19-a422e44d6fd4/download",
    "dl_167": "https://openknowledge.worldbank.org/bitstreams/9ed455e8-7c14-4261-a396-49b82603abde/download",
    "dl_168": "https://openknowledge.worldbank.org/bitstreams/4cd7e94d-e280-4a8f-ac31-78f322c379cd/download",
    "dl_169": "https://openknowledge.worldbank.org/bitstreams/ac8ccd3d-2fe2-55d8-bea3-a2792cc873b8/download",
    "dl_170": "https://openknowledge.worldbank.org/bitstreams/f0628447-325a-53a4-a427-7d1e41587f6f/download",
    "dl_171": "https://openknowledge.worldbank.org/bitstreams/49c53735-3bbf-47a8-86be-7277e719998e/download",
    "dl_172": "https://openknowledge.worldbank.org/bitstreams/60a6634d-df1c-574d-80ab-4725d6169781/download",
    "dl_173": "https://openknowledge.worldbank.org/bitstreams/31675794-ab9a-5466-9e46-6608cc6dab64/download",
    "dl_174": "https://openknowledge.worldbank.org/bitstreams/7c81ff9b-6f43-5648-be15-b2e2b25d1d33/download",
    "dl_175": "https://openknowledge.worldbank.org/bitstreams/d6678f0c-d860-559b-99fa-e31ab663cd95/download",
    "dl_176": "https://openknowledge.worldbank.org/bitstreams/e91f4c4e-a61b-507d-bb91-a39c5ad2f499/download",
    "dl_177": "https://openknowledge.worldbank.org/bitstreams/96bdc753-97a2-58dc-8bbf-564bf3d6117c/download",
    "dl_178": "https://openknowledge.worldbank.org/bitstreams/bd57a272-42f1-56ee-a3cb-44e46e7f9aa4/download",
    "dl_179": "https://openknowledge.worldbank.org/bitstreams/f49edf2d-332d-563b-89ec-ad2932846029/download",
    "dl_180": "https://openknowledge.worldbank.org/bitstreams/8ff1c67a-12c7-5b19-bcd6-bb89d3f14d87/download",
    "dl_181": "https://openknowledge.worldbank.org/bitstreams/52409ffd-96f7-58d4-be7f-c8114abbd4c5/download",
    "dl_182": "https://openknowledge.worldbank.org/bitstreams/2b9a25b1-f244-53cd-a6ff-73f12ba8c22c/download",
    "dl_183": "https://openknowledge.worldbank.org/bitstreams/97882814-9c1c-42a7-aad8-2e1c0cdbb533/download",
    "dl_184": "https://openknowledge.worldbank.org/bitstreams/9c9764c1-076d-5dcc-8339-6e4f0de2b610/download",
    "dl_185": "https://openknowledge.worldbank.org/bitstreams/08ab66bc-6f69-463f-aa77-4e852db44f4c/download",
    "dl_186": "https://openknowledge.worldbank.org/bitstreams/6d66e133-e49d-5ad9-b056-7b1a6c6206ed/download",
    "dl_187": "https://openknowledge.worldbank.org/bitstreams/0f1eac4d-2350-5a09-a1fc-bad652dff6cb/download",
    "dl_188": "https://openknowledge.worldbank.org/bitstreams/568ad9f5-06a9-5400-ab9e-274677530800/download",
    "dl_189": "https://openknowledge.worldbank.org/bitstreams/119e415d-92c7-5cb1-aea3-ad40f1c9e7e8/download",
    "dl_190": "https://openknowledge.worldbank.org/bitstreams/c9931e4b-efb0-5f94-af73-8744c0d74db1/download",
    "dl_191": "https://openknowledge.worldbank.org/bitstreams/c5c11886-30bf-5350-8e5f-df9722b85fe0/download",
    "dl_192": "https://openknowledge.worldbank.org/bitstreams/db0a50ce-42af-5266-ba82-7f946a1ecf29/download",
    "dl_193": "https://openknowledge.worldbank.org/bitstreams/0a549cdc-c5c8-53a0-a570-078800be7e02/download",
    "dl_194": "https://openknowledge.worldbank.org/bitstreams/99c4192d-d7e2-52b6-9669-827e9b11fa77/download",
    "dl_195": "https://openknowledge.worldbank.org/bitstreams/5fa150d1-45ee-5aa4-ac9d-af9b40aa3f8b/download",
    "dl_196": "https://openknowledge.worldbank.org/bitstreams/35ea9337-dfcf-5d60-9806-65913459d928/download",
    "dl_197": "https://openknowledge.worldbank.org/bitstreams/98a31afc-f0e2-5cad-8380-2473ba85ba29/download",
    "dl_198": "https://openknowledge.worldbank.org/bitstreams/3cf6d04a-d16f-46de-9d09-09d50cdefad8/download",
    "dl_199": "https://openknowledge.worldbank.org/bitstreams/a06d8703-5486-5345-90e3-c58c1c69b2f4/download",
    "dl_200": "https://openknowledge.worldbank.org/bitstreams/9d44cb89-279d-5ede-a28a-89ffe54949b9/download",
    "dl_201": "https://openknowledge.worldbank.org/bitstreams/bbcae1ac-127f-5219-a490-c80012bfea8f/download",
    "dl_202": "https://openknowledge.worldbank.org/bitstreams/4ddbc044-5fe5-5306-90ee-de51037b017e/download",
    "dl_203": "https://openknowledge.worldbank.org/bitstreams/a3aa5ce6-7149-5a82-949c-0d3157bc6881/download",
    "dl_204": "https://openknowledge.worldbank.org/bitstreams/130bab71-586e-5d48-8fd3-b7fad17fe4e9/download",
    "dl_205": "https://openknowledge.worldbank.org/bitstreams/23693e02-37d4-57b3-b630-acb37e93a5fd/download",
    "dl_206": "https://openknowledge.worldbank.org/bitstreams/cafb4b4c-c080-5b6a-aa02-4015a9474f0b/download",
    "dl_207": "https://openknowledge.worldbank.org/bitstreams/8b4dc9e2-ef7a-523c-bf2a-911838caa20c/download",
    "dl_208": "https://openknowledge.worldbank.org/bitstreams/c11722e6-77f4-4fa3-93c5-04453aa55bf6/download",
    "dl_209": "https://openknowledge.worldbank.org/bitstreams/b7f9d77f-aff8-4d52-a3cb-f717121944a4/download",
    "dl_210": "https://openknowledge.worldbank.org/bitstreams/30a1cb25-232c-41ab-bd96-7046d446c2fc/download",
    "dl_211": "https://openknowledge.worldbank.org/bitstreams/e693dfa1-6db4-549f-9863-38f0ecfa2ed6/download",
    "dl_212": "https://openknowledge.worldbank.org/bitstreams/ce0133de-58dd-555d-9ae9-ad67e0a157be/download",
    "dl_227": "https://openknowledge.worldbank.org/bitstreams/9deeaf4b-a936-5e56-9397-21780f1d764d/download",
    "dl_228": "https://openknowledge.worldbank.org/bitstreams/f37a6463-152d-4cc2-a32d-467f8c14dedd/download",
    "dl_229": "https://openknowledge.worldbank.org/bitstreams/235cacc0-26d8-57c1-888a-5012327823e8/download",
    "dl_230": "https://openknowledge.worldbank.org/bitstreams/b22cb94b-42e7-5800-846d-4d90435d3a9b/download",
    "dl_231": "https://openknowledge.worldbank.org/bitstreams/99772ed7-bdb5-5502-9f5a-7cec14e944f9/download",
    "dl_232": "https://openknowledge.worldbank.org/bitstreams/544977ea-b5f7-5435-91db-fecc0c30ce5d/download",
    "dl_233": "https://openknowledge.worldbank.org/bitstreams/17ffddb1-d06b-5411-a322-9634f2325492/download",
    "dl_234": "https://openknowledge.worldbank.org/bitstreams/c8bc246d-edc3-5a23-8067-674404f296cf/download"
}

DOCUMENT_CITATIONS = {
    "dl_001": "WBG, \"Cabo Verde CCDR\", 2025",
    "dl_002": "WBG, \"Cabo Verde CCDR\", 2025",
    "dl_003": "WBG, \"Tanzania CCDR\", 2024",
    "dl_004": "WBG, \"Tanzania CCDR\", 2024",
    "dl_005": "WBG, \"Tanzania CCDR\", 2024",
    "dl_006": "WBG, \"Tanzania CCDR\", 2024",
    "dl_007": "WBG, \"Tanzania CCDR\", 2024",
    "dl_008": "WBG, \"Yemen CCDR\", 2024",
    "dl_009": "WBG, \"Yemen CCDR\", 2024",
    "dl_010": "WBG, \"Djibouti CCDR\", 2024",
    "dl_011": "WBG, \"Djibouti CCDR\", 2024",
    "dl_012": "WBG, \"Djibouti CCDR\", 2024",
    "dl_013": "WBG, \"Djibouti CCDR\", 2024",
    "dl_014": "WBG, \"Djibouti CCDR\", 2024",
    "dl_015": "WBG, \"Moldova CCDR\", 2024",
    "dl_016": "WBG, \"Moldova CCDR\", 2024",
    "dl_017": "WBG, \"Armenia CCDR\", 2024",
    "dl_018": "WBG, \"Armenia CCDR\", 2024",
    "dl_019": "WBG, \"Tajikistan CCDR\", 2024",
    "dl_020": "WBG, \"Tajikistan CCDR\", 2024",
    "dl_021": "WBG, \"Tajikistan CCDR\", 2024",
    "dl_022": "WBG, \"Tajikistan CCDR\", 2024",
    "dl_023": "WBG, \"Senegal CCDR\", 2024",
    "dl_024": "WBG, \"Senegal CCDR\", 2024",
    "dl_025": "WBG, \"Senegal CCDR\", 2024",
    "dl_026": "WBG, \"Senegal CCDR\", 2024",
    "dl_027": "WBG, \"Senegal CCDR\", 2024",
    "dl_028": "WBG, \"Poland CCDR\", 2024",
    "dl_029": "WBG, \"Poland CCDR\", 2024",
    "dl_030": "WBG, \"Madagascar CCDR\", 2024",
    "dl_031": "WBG, \"Madagascar CCDR\", 2024",
    "dl_032": "WBG, \"Madagascar CCDR\", 2024",
    "dl_033": "WBG, \"Madagascar CCDR\", 2024",
    "dl_034": "WBG, \"Madagascar CCDR\", 2024",
    "dl_035": "WBG, \"Guinea-Bissau CCDR\", 2024",
    "dl_036": "WBG, \"Guinea-Bissau CCDR\", 2024",
    "dl_037": "WBG, \"Guinea-Bissau CCDR\", 2024",
    "dl_038": "WBG, \"Central African Republic CCDR\", 2024",
    "dl_039": "WBG, \"Central African Republic CCDR\", 2024",
    "dl_040": "WBG, \"Central African Republic CCDR\", 2024",
    "dl_041": "WBG, \"Mongolia CCDR\", 2024",
    "dl_042": "WBG, \"Mongolia CCDR\", 2024",
    "dl_043": "WBG, \"Mongolia CCDR\", 2024",
    "dl_044": "WBG, \"Mongolia CCDR\", 2024",
    "dl_045": "WBG, \"Mongolia CCDR\", 2024",
    "dl_046": "WBG, \"The Pacific Atoll Countries CCDR\", 2024",
    "dl_047": "WBG, \"The Pacific Atoll Countries CCDR\", 2024",
    "dl_048": "WBG, \"The Pacific Atoll Countries CCDR\", 2024",
    "dl_049": "WBG, \"Dominica, Grenada, Saint Lucia, and Saint Vincent and the Grenadines CCDR\", 2024",
    "dl_050": "WBG, \"Dominica, Grenada, Saint Lucia, and Saint Vincent and the Grenadines CCDR\", 2024",
    "dl_051": "WBG, \"Dominica, Grenada, Saint Lucia, and Saint Vincent and the Grenadines CCDR\", 2024",
    "dl_052": "WBG, \"Dominica, Grenada, Saint Lucia, and Saint Vincent and the Grenadines CCDR\", 2024",
    "dl_053": "WBG, \"Dominica, Grenada, Saint Lucia, and Saint Vincent and the Grenadines CCDR\", 2024",
    "dl_054": "WBG, \"Ecuador CCDR\", 2024",
    "dl_055": "WBG, \"Ecuador CCDR\", 2024",
    "dl_056": "WBG, \"Ecuador CCDR\", 2024",
    "dl_057": "WBG, \"Ecuador CCDR\", 2024",
    "dl_058": "WBG, \"Western Balkans 6 CCDR\", 2024",
    "dl_059": "WBG, \"Western Balkans 6 CCDR\", 2024",
    "dl_060": "WBG, \"Western Balkans 6 CCDR\", 2024",
    "dl_061": "WBG, \"Western Balkans 6 CCDR\", 2024",
    "dl_062": "WBG, \"Western Balkans 6 CCDR\", 2024",
    "dl_063": "WBG, \"Maldives CCDR\", 2024",
    "dl_064": "WBG, \"Maldives CCDR\", 2024",
    "dl_065": "WBG, \"Maldives CCDR\", 2024",
    "dl_066": "WBG, \"Maldives CCDR\", 2024",
    "dl_067": "WBG, \"Maldives CCDR\", 2024",
    "dl_068": "WBG, \"Liberia Country Climate Development Report\", 2024",
    "dl_069": "WBG, \"Liberia Country Climate Development Report\", 2024",
    "dl_070": "WBG, \"Liberia Country Climate Development Report\", 2024",
    "dl_071": "WBG, \"Lebanon CCDR\", 2024",
    "dl_072": "WBG, \"Lebanon CCDR\", 2024",
    "dl_073": "WBG, \"Zimbabwe CCDR\", 2024",
    "dl_074": "WBG, \"Zimbabwe CCDR\", 2024",
    "dl_075": "WBG, \"Ethiopia CCDR, February 2024\", 2024",
    "dl_076": "WBG, \"Ethiopia CCDR, February 2024\", 2024",
    "dl_077": "WBG, \"Ethiopia CCDR, February 2024\", 2024",
    "dl_078": "WBG, \"MENA CCDR: Climate Change Action in the Middle East and North Africa \u2014 Key Insights from CCDRs\", 2023",
    "dl_079": "WBG, \"Benin CCDR\", 2023",
    "dl_080": "WBG, \"Benin CCDR\", 2023",
    "dl_081": "WBG, \"Benin CCDR\", 2023",
    "dl_082": "WBG, \"Benin CCDR\", 2023",
    "dl_083": "WBG, \"Dominican Republic CCDR\", 2023",
    "dl_084": "WBG, \"Dominican Republic CCDR\", 2023",
    "dl_085": "WBG, \"Dominican Republic CCDR\", 2023",
    "dl_086": "WBG, \"Dominican Republic CCDR\", 2023",
    "dl_087": "WBG, \"Dominican Republic CCDR\", 2023",
    "dl_088": "WBG, \"West Bank and Gaza CCDR\", 2023",
    "dl_089": "WBG, \"West Bank and Gaza CCDR\", 2023",
    "dl_090": "WBG, \"Tunisia CCDR\", 2023",
    "dl_091": "WBG, \"Tunisia CCDR\", 2023",
    "dl_092": "WBG, \"Tunisia CCDR\", 2023",
    "dl_093": "WBG, \"Tunisia CCDR\", 2023",
    "dl_094": "WBG, \"Tunisia CCDR\", 2023",
    "dl_095": "WBG, \"Azerbaijan CCDR\", 2023",
    "dl_096": "WBG, \"Azerbaijan CCDR\", 2023",
    "dl_097": "WBG, \"Azerbaijan CCDR\", 2023",
    "dl_098": "WBG, \"Uzbekistan CCDR\", 2023",
    "dl_099": "WBG, \"Uzbekistan CCDR\", 2023",
    "dl_100": "WBG, \"Uzbekistan CCDR\", 2023",
    "dl_101": "WBG, \"Democratic Republic of Congo (DRC) CCDR\", 2023",
    "dl_102": "WBG, \"Democratic Republic of Congo (DRC) CCDR\", 2023",
    "dl_103": "WBG, \"Democratic Republic of Congo (DRC) CCDR\", 2023",
    "dl_104": "WBG, \"Democratic Republic of Congo (DRC) CCDR\", 2023",
    "dl_105": "WBG, \"Kenya CCDR\", 2023",
    "dl_106": "WBG, \"Kenya CCDR\", 2023",
    "dl_107": "WBG, \"Kenya CCDR\", 2023",
    "dl_108": "WBG, \"Kenya CCDR\", 2023",
    "dl_109": "WBG, \"Kenya CCDR\", 2023",
    "dl_110": "WBG, \"C\u00f4te d\u2019Ivoire CCDR\", 2023",
    "dl_111": "WBG, \"C\u00f4te d\u2019Ivoire CCDR\", 2023",
    "dl_112": "WBG, \"C\u00f4te d\u2019Ivoire CCDR\", 2023",
    "dl_113": "WBG, \"C\u00f4te d\u2019Ivoire CCDR\", 2023",
    "dl_114": "WBG, \"C\u00f4te d\u2019Ivoire CCDR\", 2023",
    "dl_115": "WBG, \"Romania CCDR\", 2023",
    "dl_116": "WBG, \"Romania CCDR\", 2023",
    "dl_117": "WBG, \"Romania CCDR\", 2023",
    "dl_118": "WBG, \"Cambodia CCDR\", 2023",
    "dl_119": "WBG, \"Cambodia CCDR\", 2023",
    "dl_120": "WBG, \"Cambodia CCDR\", 2023",
    "dl_121": "WBG, \"Republic of Congo CCDR - Diversifying Congo's Economy: Making the Most of Climate Change\", 2023",
    "dl_122": "WBG, \"Republic of Congo CCDR - Diversifying Congo's Economy: Making the Most of Climate Change\", 2023",
    "dl_123": "WBG, \"Republic of Congo CCDR - Diversifying Congo's Economy: Making the Most of Climate Change\", 2023",
    "dl_124": "WBG, \"Colombia CCDR\", 2023",
    "dl_125": "WBG, \"Colombia CCDR\", 2023",
    "dl_126": "WBG, \"Colombia CCDR\", 2023",
    "dl_127": "WBG, \"Colombia CCDR\", 2023",
    "dl_128": "WBG, \"Mozambique CCDR\", 2023",
    "dl_129": "WBG, \"Mozambique CCDR\", 2023",
    "dl_130": "WBG, \"Mozambique CCDR\", 2023",
    "dl_131": "WBG, \"Honduras CCDR\", 2023",
    "dl_132": "WBG, \"Honduras CCDR\", 2023",
    "dl_133": "WBG, \"Honduras CCDR\", 2023",
    "dl_134": "WBG, \"Honduras CCDR\", 2023",
    "dl_135": "WBG, \"Honduras CCDR\", 2023",
    "dl_136": "WBG, \"Brazil CCDR\", 2023",
    "dl_137": "WBG, \"Brazil CCDR\", 2023",
    "dl_138": "WBG, \"Brazil CCDR\", 2023",
    "dl_139": "WBG, \"Brazil CCDR\", 2023",
    "dl_140": "WBG, \"Brazil CCDR\", 2023",
    "dl_141": "WBG, \"Indonesia CCDR\", 2023",
    "dl_142": "WBG, \"Indonesia CCDR\", 2023",
    "dl_143": "WBG, \"Indonesia CCDR\", 2023",
    "dl_144": "WBG, \"Indonesia CCDR\", 2023",
    "dl_145": "WBG, \"Indonesia CCDR\", 2023",
    "dl_146": "WBG, \"Egypt CCDR\", 2022",
    "dl_147": "WBG, \"Egypt CCDR\", 2022",
    "dl_148": "WBG, \"Egypt CCDR\", 2022",
    "dl_149": "WBG, \"Egypt CCDR\", 2022",
    "dl_150": "WBG, \"Egypt CCDR\", 2022",
    "dl_151": "WBG, \"Argentina CCDR\", 2022",
    "dl_152": "WBG, \"Argentina CCDR\", 2022",
    "dl_153": "WBG, \"Argentina CCDR\", 2022",
    "dl_154": "WBG, \"Argentina CCDR\", 2022",
    "dl_155": "WBG, \"Argentina CCDR\", 2022",
    "dl_156": "WBG, \"Iraq CCDR\", 2022",
    "dl_157": "WBG, \"Iraq CCDR\", 2022",
    "dl_158": "WBG, \"Iraq CCDR\", 2022",
    "dl_159": "WBG, \"Philippines CCDR\", 2022",
    "dl_160": "WBG, \"Philippines CCDR\", 2022",
    "dl_161": "WBG, \"Philippines CCDR\", 2022",
    "dl_162": "WBG, \"Philippines CCDR\", 2022",
    "dl_163": "WBG, \"Philippines CCDR\", 2022",
    "dl_164": "WBG, \"Pakistan CCDR\", 2022",
    "dl_165": "WBG, \"Pakistan CCDR\", 2022",
    "dl_166": "WBG, \"Pakistan CCDR\", 2022",
    "dl_167": "WBG, \"Pakistan CCDR\", 2022",
    "dl_168": "WBG, \"Pakistan CCDR\", 2022",
    "dl_169": "WBG, \"Peru CCDR\", 2022",
    "dl_170": "WBG, \"Peru CCDR\", 2022",
    "dl_171": "WBG, \"Peru CCDR\", 2022",
    "dl_172": "WBG, \"Peru CCDR\", 2022",
    "dl_173": "WBG, \"Peru CCDR\", 2022",
    "dl_174": "WBG, \"Jordan CCDR\", 2022",
    "dl_175": "WBG, \"Jordan CCDR\", 2022",
    "dl_176": "WBG, \"Kazakhstan CCDR\", 2022",
    "dl_177": "WBG, \"Kazakhstan CCDR\", 2022",
    "dl_178": "WBG, \"Kazakhstan CCDR\", 2022",
    "dl_179": "WBG, \"Kazakhstan CCDR\", 2022",
    "dl_180": "WBG, \"Kazakhstan CCDR\", 2022",
    "dl_181": "WBG, \"South Africa CCDR\", 2022",
    "dl_182": "WBG, \"South Africa CCDR\", 2022",
    "dl_183": "WBG, \"South Africa CCDR\", 2022",
    "dl_184": "WBG, \"Ghana CCDR\", 2022",
    "dl_185": "WBG, \"Ghana CCDR\", 2022",
    "dl_186": "WBG, \"Bangladesh CCDR\", 2022",
    "dl_187": "WBG, \"Bangladesh CCDR\", 2022",
    "dl_188": "WBG, \"Bangladesh CCDR\", 2022",
    "dl_189": "WBG, \"Bangladesh CCDR\", 2022",
    "dl_190": "WBG, \"Bangladesh CCDR\", 2022",
    "dl_191": "WBG, \"Morocco CCDR\", 2022",
    "dl_192": "WBG, \"Morocco CCDR\", 2022",
    "dl_193": "WBG, \"Morocco CCDR\", 2022",
    "dl_194": "WBG, \"Morocco CCDR\", 2022",
    "dl_195": "WBG, \"Morocco CCDR\", 2022",
    "dl_196": "WBG, \"China CCDR\", 2022",
    "dl_197": "WBG, \"China CCDR\", 2022",
    "dl_198": "WBG, \"China CCDR\", 2022",
    "dl_199": "WBG, \"China CCDR\", 2022",
    "dl_200": "WBG, \"China CCDR\", 2022",
    "dl_201": "WBG, \"Malawi CCDR\", 2022",
    "dl_202": "WBG, \"Malawi CCDR\", 2022",
    "dl_203": "WBG, \"Malawi CCDR\", 2022",
    "dl_204": "WBG, \"Malawi CCDR\", 2022",
    "dl_205": "WBG, \"Malawi CCDR\", 2022",
    "dl_206": "WBG, \"Rwanda CCDR\", 2022",
    "dl_207": "WBG, \"Rwanda CCDR\", 2022",
    "dl_208": "WBG, \"Rwanda CCDR\", 2022",
    "dl_209": "WBG, \"Nepal CCDR\", 2022",
    "dl_210": "WBG, \"Nepal CCDR\", 2022",
    "dl_211": "WBG, \"Nepal CCDR\", 2022",
    "dl_212": "WBG, \"Nepal CCDR\", 2022",
    "dl_213": "WBG, \"Vietnam CCDR\", 2022",
    "dl_214": "WBG, \"Vietnam CCDR\", 2022",
    "dl_215": "WBG, \"Vietnam CCDR\", 2022",
    "dl_216": "WBG, \"Vietnam CCDR\", 2022",
    "dl_217": "WBG, \"Vietnam CCDR\", 2022",
    "dl_218": "WBG, \"G5 Sahel Region CCDR\", 2022",
    "dl_219": "WBG, \"G5 Sahel Region CCDR\", 2022",
    "dl_220": "WBG, \"G5 Sahel Region CCDR\", 2022",
    "dl_221": "WBG, \"G5 Sahel Region CCDR\", 2022",
    "dl_222": "WBG, \"T\u00fcrkiye CCDR\", 2022",
    "dl_223": "WBG, \"T\u00fcrkiye CCDR\", 2022",
    "dl_224": "WBG, \"T\u00fcrkiye CCDR\", 2022",
    "dl_225": "WBG, \"T\u00fcrkiye CCDR\", 2022",
    "dl_226": "WBG, \"T\u00fcrkiye CCDR\", 2022",
    "dl_227": "WBG, \"Cameroon CCDR\", 2022",
    "dl_228": "WBG, \"Cameroon CCDR\", 2022",
    "dl_229": "WBG, \"Cameroon CCDR\", 2022",
    "dl_230": "WBG, \"Angola CCDR\", 2022",
    "dl_231": "WBG, \"Angola CCDR\", 2022",
    "dl_232": "WBG, \"Angola CCDR\", 2022",
    "dl_233": "WBG, \"Angola CCDR\", 2022",
    "dl_234": "WBG, \"Angola CCDR\", 2022"
}