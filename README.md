# AI Document QA

Local RAG chatbot that reads a public Google Doc and answers questions from the document only.

## Stack

- Python
- sentence-transformers
- FAISS
- Ollama
- phi3
- requests

## Setup

Create and activate a Python 3.10, 3.11, or 3.12 virtual environment.

```powershell
python -m venv .venv312
.venv312\Scripts\python.exe -m pip install -r requirements.txt
```

Install and start Ollama, then pull the local model.

```powershell
ollama pull phi3
```

## Run

```powershell
.venv312\Scripts\python.exe main.py
```

Type a question, or type `exit` to quit.

If the answer is not in the document, the chatbot responds:

```text
Not found in document
```
