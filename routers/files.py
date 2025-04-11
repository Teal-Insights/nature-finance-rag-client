import os
import logging
from typing import List, Dict
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, Path
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from openai import AsyncOpenAI
from exceptions.http_exceptions import OpenAIError
from utils.chat.sse import stream_file_content

logger = logging.getLogger("uvicorn.error")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Check if environment variables are missing
load_dotenv(override=True)
assistant_id_env_var: str | None = os.getenv("ASSISTANT_ID")

if not assistant_id_env_var:
    raise OpenAIError("OpenAI API key or assistant ID is missing")
else:
    assistant_id: str = assistant_id_env_var

router = APIRouter(
    prefix="/chat/files",
    tags=["chat_files"]
)

# Helper function to get or create a vector store
async def get_vector_store(assistantId: str, client: AsyncOpenAI = Depends(lambda: AsyncOpenAI())) -> str:
    assistant = await client.beta.assistants.retrieve(assistantId)
    if assistant.tool_resources and assistant.tool_resources.file_search and assistant.tool_resources.file_search.vector_store_ids:
        return assistant.tool_resources.file_search.vector_store_ids[0]
    raise HTTPException(status_code=404, detail="Vector store not found")


@router.get("/")
async def list_files(client: AsyncOpenAI = Depends(lambda: AsyncOpenAI())) -> List[Dict[str, str]]:
    # List files in the vector store
    vector_store_id = await get_vector_store(assistant_id, client)
    file_list = await client.vector_stores.files.list(vector_store_id)
    files_array: List[Dict[str, str]] = []
    
    if file_list.data:
        for file in file_list.data:
            file_details = await client.files.retrieve(file.id)
            vector_file_details = await client.vector_stores.files.retrieve(
                vector_store_id=vector_store_id,
                file_id=file.id
            )
            files_array.append({
                "file_id": file.id,
                "filename": file_details.filename or "unknown_filename",
                "status": vector_file_details.status or "unknown_status",
            })
    return files_array


@router.get("/{file_id}")
async def get_file(
    file_id: str = Path(..., description="The ID of the file to retrieve"),
    client: AsyncOpenAI = Depends(lambda: AsyncOpenAI())
) -> StreamingResponse:
    try:
        file = await client.files.retrieve(file_id)
        file_content = await client.files.content(file_id)
        
        if not hasattr(file_content, 'content'):
            raise HTTPException(status_code=500, detail="File content not available")
            
        return StreamingResponse(
            stream_file_content(file_content.content),
            headers={"Content-Disposition": f'attachment; filename=\"{file.filename or "download"}\"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{file_id}/content")
async def get_file_content(
    file_id: str,
    client: AsyncOpenAI = Depends(lambda: AsyncOpenAI())
) -> StreamingResponse:
    """
    Streams file content from OpenAI API.
    This route is used to serve images and other files generated by the code interpreter.
    """
    try:
        # Get the file content from OpenAI
        file_content = await client.files.content(file_id)
        file_bytes = file_content.read()  # Remove await since read() returns bytes directly
        
        # Return the file content as a streaming response
        # Note: In a production environment, you might want to add caching
        return StreamingResponse(
            content=iter([file_bytes]),
            media_type="image/png"  # You might want to make this dynamic based on file type
        )
    except Exception as e:
        logger.error(f"Error getting file content: {e}")
        raise HTTPException(status_code=500, detail=str(e))
