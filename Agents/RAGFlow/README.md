# RAG Pipeline in Langflow

Simple Retrieval-Augmented Generation (RAG) pipeline built in Langflow using:
- OpenAI Embeddings
- Chroma Vector Database
- Document Chunking
- Semantic Retrieval

---

# Pipeline Overview

The pipeline consists of two separate flows:

## 1. Document Ingestion Flow

This flow is responsible for:
- loading uploaded documents,
- splitting them into chunks,
- generating embeddings,
- and storing them inside the vector database.

```
File
↓
Split Text
↓
OpenAI Embeddings
↓
Chroma Vector Store
```

## 2. Retrieval + Generation Flow

This flow performs the actual RAG process:
- receives the user question,
- retrieves relevant chunks from Chroma,
- injects them into the prompt,
- and generates the final answer.
```
User Question
↓
Similarity Search
↓
Retrieved Context
↓
Prompt Template
↓
LLM Responseesponse
```

## Flow Visualization

![RAG Flow](image/RAGFlow.png)

## Main Components

| Component | Purpose |
|---|---|
| File | Loads uploaded documents |
| Split Text | Splits documents into smaller chunks |
| OpenAI Embeddings | Converts text into vector embeddings |
| Chroma DB | Stores embeddings and performs semantic retrieval |
| Parser | Converts retrieved chunks into prompt context |
| Prompt | Builds the final prompt for the LLM |
| OpenAI Chat Model | Generates the final answer |
| Chat Input / Output | User interaction layer |

The user query is embedded, relevant chunks are retrieved from Chroma, and the LLM generates an answer using the retrieved context.
