import type { Config } from "drizzle-kit";
import { env } from "@/lib/env.mjs";

export default {
  dialect: "postgresql",
  dbCredentials: {
    url: env.DATABASE_URL,
  }
} satisfies Config;