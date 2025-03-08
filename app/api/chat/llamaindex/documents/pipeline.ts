import {
  Document,
  IngestionPipeline,
  Settings,
  SentenceSplitter,
  storageContextFromDefaults,
  VectorStoreIndex,
  MetadataMode,
} from "llamaindex";
import { MistralAIEmbedding } from "@llamaindex/mistral";

export async function runPipeline(
  currentIndex: VectorStoreIndex | null,
  documents: Document[],
) {
  // Use ingestion pipeline to process the documents into nodes and add them to the vector store
  const pipeline = new IngestionPipeline({
    transformations: [
      new SentenceSplitter({
        chunkSize: Settings.chunkSize,
        chunkOverlap: Settings.chunkOverlap,
      }),
    ],
  });
  
  // Process documents to create nodes
  const nodes = await pipeline.run({ documents });
  
  // Apply embeddings separately
  try {
    console.log("Processing embeddings...");
    
    // Use the exact same pattern that works in the test file
    const embeddingModel = new MistralAIEmbedding({
      apiKey: process.env.MISTRAL_API_KEY
    });
    
    // Process each node individually
    for (const node of nodes) {
      const text = node.getContent(MetadataMode.EMBED);
      try {
        console.log(`Getting embedding for text of length: ${text.length}`);
        const embeddings = await embeddingModel.getTextEmbedding(text);
        console.log(`Successfully retrieved embedding of length: ${embeddings.length}`);
        node.embedding = embeddings;
      } catch (embeddingError) {
        console.error("Embedding error details:", embeddingError);
        // Continue without embedding this node
        console.log("Continuing without embedding for this node");
      }
    }
  } catch (error) {
    console.error("Error generating embeddings:", error);
    // Continue without embeddings
  }
  if (currentIndex) {
    await currentIndex.insertNodes(nodes);
    currentIndex.storageContext.docStore.persist();
    console.log("Added nodes to the vector store.");
    return documents.map((document) => document.id_);
  } else {
    // Initialize a new index with the documents
    console.log(
      "Got empty index, created new index with the uploaded documents",
    );
    const persistDir = process.env.STORAGE_CACHE_DIR;
    if (!persistDir) {
      throw new Error("STORAGE_CACHE_DIR environment variable is required!");
    }
    const storageContext = await storageContextFromDefaults({
      persistDir,
    });
    const newIndex = await VectorStoreIndex.fromDocuments(documents, {
      storageContext,
    });
    await newIndex.storageContext.docStore.persist();
    return documents.map((document) => document.id_);
  }
}
