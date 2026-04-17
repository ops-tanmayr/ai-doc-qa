# AI Document Question Answering System

This is a Python-based RAG chatbot that reads a Google Doc and answers questions from that document only.

If the answer is not available in the document, the chatbot returns:

```text
Not found in document
```

## What It Does

- Reads text from a Google Doc
- Splits the text into smaller chunks
- Creates embeddings using `sentence-transformers`
- Stores embeddings in FAISS
- Finds the most relevant chunks for a user question
- Sends the question and document context to a local Ollama model
- Answers only from the document context

## Tech Stack

- Python
- requests
- sentence-transformers
- FAISS
- Ollama
- Phi3

## Flow

```text
Google Doc
-> Fetch text
-> Split into chunks
-> Create embeddings
-> Store in FAISS
-> User asks question
-> Retrieve relevant chunks
-> Send context to Phi3 using Ollama
-> Return answer
```

## Google Doc Reading

There are two ways to read the Google Doc.

### Option 1: Public Google Doc Link

This project currently uses a public Google Doc export URL:

```text
https://docs.google.com/document/d/<DOC_ID>/export?format=txt
```

The document must be shared publicly for this method to work.

### Option 2: Google Docs API

Google Docs API can also be used to read private documents.

This needs:

- Google Cloud Project
- Google Docs API enabled
- OAuth or service account credentials
- Access permission for the document

The rest of the RAG flow remains the same after the document text is fetched.

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

Install Ollama:

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

Exit:

```text
exit
```

## Example Questions

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

If the question is outside the document:

```text
What is the capital of France?
```

Expected answer:

```text
Not found in document
```

## Files

- `main.py`: Main RAG chatbot script
- `requirements.txt`: Python dependencies
- `.gitignore`: Files and folders ignored by Git

## Notes

- The current version uses a public Google Doc link.
- The local LLM runs through Ollama.
- FAISS index is created when the script starts.
- No paid API is required.
