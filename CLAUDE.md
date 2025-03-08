# econ-rag Development Guidelines

## Description
Econ-RAG is a tool for semantic search and question-answering over methodological documentation from sovereign credit ratings agencies. This repository is an exploratory proof of concept built with LlamaIndex and Mistral.

## Build & Development Commands
- `bun run dev` - Start the development server
- `bun run build` - Build for production
- `bun run start` - Start the production server
- `bun run lint` - Run ESLint
- `bun run format` - Check formatting with Prettier
- `bun run format:write` - Fix formatting issues
- `bun run generate` - Generate storage context with documents

## Code Style Guidelines
- **Imports**: Use `prettier-plugin-organize-imports` for auto-organization
- **Formatting**: Follow Prettier defaults; use `npm run format:write` before commits
- **TypeScript**: Use strict mode with explicit typing for function params and returns
- **React Components**: Use functional components with explicit prop types
- **Error Handling**: Use try/catch blocks with specific error types
- **Naming**: PascalCase for components, camelCase for functions/variables
- **File Structure**: Group related functionality in directories (engine/, tools/)
- **State Management**: Use React hooks (useState, useContext) for state