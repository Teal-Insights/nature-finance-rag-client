import { MistralAIEmbedding } from "@llamaindex/mistral";
import * as dotenv from "dotenv";

// Load environment variables
dotenv.config();

async function testEmbeddings() {
  try {
    console.log("Creating MistralAIEmbedding instance...");
    const embedding = new MistralAIEmbedding({
      apiKey: process.env.MISTRAL_API_KEY,
    });
    
    console.log("Getting embeddings for test text...");
    const text = "What is the best French cheese?";
    
    // This is the line that's failing in our application
    const embeddingsResponse = await embedding.getTextEmbedding(text);
    
    console.log(`MistralAI embeddings are ${embeddingsResponse.length} numbers long`);
    console.log("First 5 values:", embeddingsResponse.slice(0, 5));
    
    return "Success!";
  } catch (error) {
    console.error("Error in testEmbeddings:", error);
    return `Failed: ${error.message}`;
  }
}

// Self-executing async function
(async () => {
  console.log("Starting embeddings test...");
  const result = await testEmbeddings();
  console.log("Test result:", result);
})();