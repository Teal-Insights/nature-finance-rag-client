import { MistralAI, MistralAIEmbedding } from "@llamaindex/mistral";
import { Settings } from "llamaindex";

export function setupProvider() {
  Settings.llm = new MistralAI({
    model: process.env.MODEL ?? "mistral-tiny",
    apiKey: process.env.MISTRAL_API_KEY,
    maxTokens: process.env.LLM_MAX_TOKENS
      ? Number(process.env.LLM_MAX_TOKENS)
      : undefined,
  });
  Settings.embedModel = new MistralAIEmbedding({
    apiKey: process.env.MISTRAL_API_KEY,
    model: process.env.EMBEDDING_MODEL,
  });
}
