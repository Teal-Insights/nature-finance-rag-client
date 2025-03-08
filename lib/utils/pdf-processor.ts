import fs from 'fs/promises';
import path from 'path';
import pdfParse from 'pdf-parse';
import { db } from '../db';
import { resources } from '../db/schema/resources';
import { generateEmbeddings } from '../ai/embedding';
import { embeddings } from '../db/schema/embeddings';

// Enhanced chunking function for PDFs
const chunkPdfText = (text: string, maxChunkSize: number = 1000): string[] => {
  // Replace multiple newlines with a single space
  const cleanText = text.replace(/\s+/g, ' ').trim();
  
  // First try to split by paragraphs (double newlines)
  let chunks: string[] = [];
  let currentChunk = '';
  
  // Split by sentences (period + space or newline)
  const sentences = cleanText.split(/\.\s+/);
  
  for (const sentence of sentences) {
    const sentenceWithPeriod = sentence.trim() + '.';
    
    if (currentChunk.length + sentenceWithPeriod.length > maxChunkSize && currentChunk.length > 0) {
      chunks.push(currentChunk.trim());
      currentChunk = sentenceWithPeriod;
    } else {
      currentChunk += ' ' + sentenceWithPeriod;
    }
  }
  
  if (currentChunk.trim()) {
    chunks.push(currentChunk.trim());
  }
  
  return chunks;
};

export async function processPdf(filePath: string): Promise<string> {
  const dataBuffer = await fs.readFile(filePath);
  const pdfData = await pdfParse(dataBuffer);
  return pdfData.text;
}

export async function processAndStorePdf(filePath: string): Promise<{ resourceId: string, chunks: number }> {
  try {
    // Extract text from PDF
    const pdfText = await processPdf(filePath);
    const fileName = path.basename(filePath);
    
    // Store the full content as a resource
    const [resource] = await db.insert(resources).values({
      content: pdfText,
      source: fileName
    }).returning();
    
    // Generate chunks
    const textChunks = chunkPdfText(pdfText);
    
    // Process each chunk and generate embeddings
    for (const chunk of textChunks) {
      const embeddingResults = await generateEmbeddings(chunk);
      
      // Store each chunk with its embedding
      for (const { content, embedding } of embeddingResults) {
        await db.insert(embeddings).values({
          resourceId: resource.id,
          content,
          embedding
        });
      }
    }
    
    return { resourceId: resource.id, chunks: textChunks.length };
  } catch (error) {
    console.error('Error processing PDF:', error);
    throw error;
  }
}

// Function to process all PDFs in a directory
export async function processAllPdfsInDirectory(directoryPath: string): Promise<Array<{ file: string, result: { resourceId: string, chunks: number } }>> {
  const files = await fs.readdir(directoryPath);
  const pdfFiles = files.filter(file => file.toLowerCase().endsWith('.pdf'));
  
  const results = [];
  
  for (const pdfFile of pdfFiles) {
    const fullPath = path.join(directoryPath, pdfFile);
    const result = await processAndStorePdf(fullPath);
    results.push({ file: pdfFile, result });
  }
  
  return results;
} 