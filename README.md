# AI Document Question Answering System

This project is a local Retrieval-Augmented Generation application that reads content from a Google Doc and answers user questions strictly from that document.

The system is designed as a simple proof of concept for document-based question answering. It does not use paid APIs for answer generation. The language model runs locally through Ollama.

## Goal

The goal is to build an interactive chatbot that can:

- Read document content from Google Docs
- Split the document into smaller text chunks
- Convert the chunks into embeddings
- Store and search embeddings using FAISS
- Send only the relevant document context to a local LLM
- Answer only from the document
- Return `Not found in document` when the answer is not available in the document

## Current Implementation

The current version uses a public Google Docs export URL.

The Google Doc is fetched using:

```python
https://docs.google.com/document/d/<DOC_ID>/export?format=txt
```

This approach is simple and works well for a proof of concept because it does not require Google Cloud setup, OAuth, service accounts, or credential management.

Current document access flow:

1. The Google Doc is made publicly readable.
2. The script downloads the document as plain text.
3. The text is processed locally.
4. The chatbot answers questions using only the retrieved document context.

## Architecture

```text
Google Doc
   |
   v
Fetch document text using public export URL
   |
   v
Split text into chunks
   |
   v
Create embeddings using sentence-transformers
   |
   v
Store embeddings in FAISS
   |
   v
User asks a question
   |
   v
Convert question into embedding
   |
   v
Retrieve relevant chunks from FAISS
   |
   v
Send context and question to Ollama Phi3
   |
   v
Return answer from document context only
```

## Tech Stack

- Python
- requests
- sentence-transformers
- FAISS
- Ollama
- Phi3 local model

## Why Ollama

Ollama is used because it allows the language model to run locally on the machine.

Benefits:

- No paid LLM API is required
- No document context is sent to an external LLM provider
- Works well for local development and proof of concept work
- Easy to switch between local models
- Simple HTTP API available at `http://localhost:11434`

In this project, the code communicates with Ollama through its local HTTP API instead of depending on the `ollama` command being available in the terminal PATH.

## Why Phi3

Phi3 is used as the local LLM for answer generation.

Reasons:

- Lightweight compared to larger models
- Can run locally through Ollama
- Good enough for simple question answering tasks
- Practical for local proof of concept development
- No cloud LLM cost

The current model name is configured in `main.py`:

```python
OLLAMA_MODEL = "phi3"
```

## Why sentence-transformers

The project uses `all-MiniLM-L6-v2` from sentence-transformers for embeddings.

Reasons:

- Lightweight and fast
- Good semantic search quality for small and medium documents
- Runs locally
- Easy to integrate with FAISS

The current embedding model is configured in `main.py`:

```python
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

## Why FAISS

FAISS is used as the vector search layer.

Reasons:

- Fast similarity search
- Runs locally
- No database server required
- Good fit for a simple local RAG proof of concept

The current implementation normalizes embeddings and uses FAISS inner product search. This works like cosine similarity for normalized vectors.

## Google Doc Access Options

There are two practical ways to read Google Docs content.

## Option 1: Public Google Doc Export URL

This is the approach used in the current project.

Pros:

- Simple to implement
- No Google Cloud setup required
- No OAuth flow required
- No service account required
- Good for proof of concept and demo projects

Cons:

- The document must be publicly readable
- Not suitable for private or sensitive documents
- Access control is limited

This approach is useful for the current submission because the focus is on proving the RAG flow end to end.

## Option 2: Google Docs API

For production or private documents, the better approach is to use the official Google Docs API.

This requires:

- Google Cloud Project
- Google Docs API enabled
- OAuth client or service account
- Credential handling
- Access permissions for the target document

Pros:

- Can read private Google Docs
- Better security
- Better access control
- More suitable for production use
- Can integrate with organization-level document access policies

Cons:

- More setup required
- Requires Google Cloud configuration
- Requires secure credential management

Recommended future direction:

Use the Google Docs API when private document access is required. The current public export URL can be replaced with a secure Google Docs API reader without changing the rest of the RAG pipeline.

## Prompting Rule

The LLM is instructed to answer only from the retrieved document context.

If the answer is not present in the context, it must return:

```text
Not found in document
```

This rule is enforced in the prompt before sending the question to Phi3.

## Setup

Use Python 3.10, 3.11, or 3.12.

Create a virtual environment:

```powershell
python -m venv .venv312
```

Install dependencies:

```powershell
.venv312\Scripts\python.exe -m pip install -r requirements.txt
```

Install Ollama from:

```text
https://ollama.com
```

Pull the Phi3 model:

```powershell
ollama pull phi3
```

Make sure Ollama is running before starting the script.

## Run

```powershell
.venv312\Scripts\python.exe main.py
```

Ask a question:

```text
What is AWS Lambda?
```

Exit the chatbot:

```text
exit
```

## Example Document Content

The current Google Doc contains AWS-related information such as:

- AWS Lambda
- IAM Role
- Amazon S3
- Amazon EC2
- Auto Scaling
- CloudWatch

Example supported questions:

```text
What is AWS Lambda?
```

```text
What is the default timeout for AWS Lambda?
```

```text
What is Amazon S3 used for?
```

```text
What is CloudWatch used for?
```

For a question outside the document, such as:

```text
What is the capital of France?
```

Expected response:

```text
Not found in document
```

## Current Limitations

- Current document access requires a public Google Doc
- No chat history is stored
- FAISS index is rebuilt every time the script starts
- No web UI is included yet
- No source citations are shown in the answer

## Recommended Next Steps

1. Add Google Docs API support for private documents.
2. Store FAISS index locally to avoid rebuilding on every run.
3. Add source chunk display with each answer.
4. Add a simple web UI using Streamlit or FastAPI.
5. Add support for multiple documents.
6. Add better logging and test cases.

## Summary

This project demonstrates a working local RAG pipeline using Google Docs, sentence-transformers, FAISS, Ollama, and Phi3.

The current implementation is intentionally simple and practical. It proves the full flow from document ingestion to retrieval to local LLM-based answering. For production use, the main upgrade should be replacing the public Google Doc export link with the Google Docs API for secure private document access.
