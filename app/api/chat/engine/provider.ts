import { MistralAI, MistralAIEmbedding, MistralAIEmbeddingModelType } from "@llamaindex/mistral";
import { Settings } from "llamaindex";

export function setupProvider() {
  console.log("Setting up Mistral provider...");
  
  Settings.llm = new MistralAI({
    model: (process.env.MODEL as "mistral-tiny" | "mistral-small" | "mistral-medium") ?? "mistral-tiny",
    apiKey: process.env.MISTRAL_API_KEY,
    maxTokens: process.env.LLM_MAX_TOKENS
      ? Number(process.env.LLM_MAX_TOKENS)
      : undefined,
  });
  
  // Explicitly use MistralAIEmbedding with correct model type
  const embeddingModel = process.env.EMBEDDING_MODEL || "mistral-embed";
  console.log(`Using embedding model: ${embeddingModel}`);
  
  Settings.embedModel = new MistralAIEmbedding({
    apiKey: process.env.MISTRAL_API_KEY,
    model: MistralAIEmbeddingModelType.MISTRAL_EMBED, // Use explicit enum value instead of string
  });
  
  console.log(`Embedding model initialized: ${Settings.embedModel.constructor.name}`);
}
