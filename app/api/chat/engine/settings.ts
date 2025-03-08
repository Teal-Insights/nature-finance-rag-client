import { Settings } from "llamaindex";
import { setupProvider } from "./provider";
import * as dotenv from "dotenv";

const CHUNK_SIZE = 512;
const CHUNK_OVERLAP = 20;

export const initSettings = async () => {
  // Explicitly load environment variables from .env file
  dotenv.config();
  
  console.log(`Using 'Mistral' model provider`);
  console.log(`MISTRAL_API_KEY exists: ${!!process.env.MISTRAL_API_KEY}`);
  console.log(`MISTRAL_API_KEY length: ${process.env.MISTRAL_API_KEY?.length || 0}`);

  if (!process.env.MISTRAL_API_KEY) {
    throw new Error("'MISTRAL_API_KEY' env variable must be set.");
  }

  // Default models if not specified in environment
  process.env.MODEL = process.env.MODEL || "mistral-tiny";
  process.env.EMBEDDING_MODEL = process.env.EMBEDDING_MODEL || "mistral-embed";

  Settings.chunkSize = CHUNK_SIZE;
  Settings.chunkOverlap = CHUNK_OVERLAP;

  setupProvider();
  
  // Add validation check after setup
  if (!Settings.embedModel) {
    throw new Error("Embedding model failed to initialize properly");
  }
};
