import { Settings } from "llamaindex";
import { setupProvider } from "./provider";

const CHUNK_SIZE = 512;
const CHUNK_OVERLAP = 20;

export const initSettings = async () => {
  console.log(`Using 'Mistral' model provider`);

  if (!process.env.MISTRAL_API_KEY) {
    throw new Error("'MISTRAL_API_KEY' env variable must be set.");
  }

  // Default models if not specified in environment
  process.env.MODEL = process.env.MODEL || "mistral-tiny";
  process.env.EMBEDDING_MODEL = process.env.EMBEDDING_MODEL || "mistral-embed";

  Settings.chunkSize = CHUNK_SIZE;
  Settings.chunkOverlap = CHUNK_OVERLAP;

  setupProvider();
};
