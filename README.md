# RAG application for credit ratings agency methodologies

This is a RAG application for credit ratings agency methodologies. It is built with Next.js, Shadcn UI, and Vercel AI SDK, with a Postgres vector database to store embeddings and retrieve relevant content.

## Getting Started

1. Clone the repository
2. Run `npm install` to install the dependencies
3. Run `docker compose up` to start the Postgres database
4. Run `npm run db:migrate` to migrate the database
5. Run `npm run ingest:pdfs` to ingest the PDFs

## Implementation

The text is chunked into paragraphs, with a max chunk length of 2500 characters.

## Chatting with the RAG application

To chat with the RAG application, run the following command:

```bash
npm run dev
```
