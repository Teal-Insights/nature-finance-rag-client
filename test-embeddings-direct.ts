import * as dotenv from "dotenv";
import { Mistral } from "@mistralai/mistralai";

// Load environment variables
dotenv.config();

async function testDirectApi() {
  try {
    console.log("Testing direct Mistral API call...");
    const client = new Mistral({
      apiKey: process.env.MISTRAL_API_KEY
    });
    
    const text = "What is the best French cheese?";
    
    // Use the direct Mistral API
    console.log("Calling embeddings.create with inputs parameter...");
    const response = await client.embeddings.create({
      model: "mistral-embed",
      inputs: [text] // Using 'inputs' instead of 'input'
    });
    
    console.log(`Direct API: embeddings are ${response.data[0].embedding.length} numbers long`);
    console.log("First 5 values:", response.data[0].embedding.slice(0, 5));
    
    return "Direct API success!";
  } catch (error) {
    console.error("Error in direct API test:", error);
    return `Direct API failed: ${error.message}`;
  }
}

// Self-executing async function
(async () => {
  console.log("Starting direct Mistral API test...");
  const result = await testDirectApi();
  console.log("Test result:", result);
})();