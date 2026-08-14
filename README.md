# Offline Multimodal RAG Assistant

An offline, multimodal RAG (Retrieval-Augmented Generation) assistant that ingests PDFs, DOCX documents, images, and audio, and answers questions with source citations, using Ollama + ChromaDB, fully local with no cloud dependency.

## Features
- **100% Offline & Private**: Runs entirely locally on your machine with no API keys or cloud services.
- **Multimodal Ingestion**: Supports PDF, DOCX, Image (OCR), and Audio (transcription) files.
- **Semantic Search**: Powered by ChromaDB and local Ollama embeddings (`nomic-embed-text`).
- **Answer Generation**: Synthesizes responses with source citations using local Ollama LLM (`llama3.2:3b`).
