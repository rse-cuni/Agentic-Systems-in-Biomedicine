# RAG Pipeline in Langflow

Simple Retrieval-Augmented Generation (RAG) pipeline built in Langflow using:
- OpenAI Embeddings
- Chroma Vector Database
- Document Chunking
- Semantic Retrieval

---

# Pipeline Overview

## Document Ingestion

```
File
↓
Split Text
↓
OpenAI Embeddings
↓
Chroma Vector Store
```
Documents are:

- loaded,
- split into chunks,
- converted into embeddings,
- and stored in a vector database.

## Retrieval + Generation
```
User Question
↓
Embedding-based Retrieval
↓
Retrieved Context
↓
Prompt Template
↓
LLM Response
```

The user query is embedded, relevant chunks are retrieved from Chroma, and the LLM generates an answer using the retrieved context.
