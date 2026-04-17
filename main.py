import os
import sys

import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer

DOC_ID = "1cPYJqbteAZGIgPobyh7skxigvBAibuPyxPGTyBRifpE"
DOC_URL = f"https://docs.google.com/document/d/{DOC_ID}/export?format=txt"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "phi3"
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
CHUNK_WORDS = 120
CHUNK_OVERLAP = 30
TOP_K = 3


def check_python_version():
    version = sys.version_info
    if version.major == 3 and version.minor in (10, 11, 12):
        return

    print(
        "Warning: this project is safest on Python 3.10, 3.11, or 3.12. "
        f"You are running Python {version.major}.{version.minor}.{version.micro}."
    )


def check_ollama_model():
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=10)
        response.raise_for_status()
    except Exception as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure Ollama is running. "
            f"Checked: {OLLAMA_HOST}"
        ) from exc

    models = response.json().get("models", [])
    model_names = {model.get("name", "") for model in models}
    model_base_names = {name.split(":", 1)[0] for name in model_names}

    if OLLAMA_MODEL not in model_names and OLLAMA_MODEL not in model_base_names:
        raise RuntimeError(
            f"Ollama model '{OLLAMA_MODEL}' is not installed. Run: ollama pull {OLLAMA_MODEL}"
        )


def fetch_doc():
    print("Fetching Google Doc...")
    response = requests.get(DOC_URL, timeout=30)
    response.raise_for_status()

    text = response.text.strip()
    if not text:
        raise ValueError("Document is empty.")

    print("Document fetched")
    return text


def chunk_text(text, chunk_words=CHUNK_WORDS, overlap=CHUNK_OVERLAP):
    print("Chunking text...")

    words = text.split()
    if not words:
        raise ValueError("No readable text found in document.")

    chunks = []
    step = max(1, chunk_words - overlap)

    for start in range(0, len(words), step):
        chunk = " ".join(words[start : start + chunk_words]).strip()
        if chunk:
            chunks.append(chunk)

        if start + chunk_words >= len(words):
            break

    print(f"Created {len(chunks)} chunks")
    return chunks


def load_embedding_model():
    print("Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("Model loaded")
    return model


def build_index(model, chunks):
    print("Creating embeddings...")
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    ).astype("float32")

    print("Building FAISS index...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    print("Index ready")
    return index


def search(model, query, index, chunks, k=TOP_K):
    query_vec = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    ).astype("float32")

    _scores, indices = index.search(query_vec, min(k, len(chunks)))
    return [chunks[i] for i in indices[0] if i >= 0]


def ask_llm(query, context_chunks):
    context = "\n\n---\n\n".join(context_chunks)

    prompt = f"""You are a document question-answering assistant.

Rules:
- Answer only from the context.
- Do not use outside knowledge.
- If the context does not contain the answer, reply exactly: Not found in document
- Keep the answer concise.

Context:
{context}

Question: {query}

Answer:"""

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()

        answer = response.json().get("response", "").strip()
        return answer or "Not found in document"

    except requests.Timeout:
        return "LLM Error: Ollama timed out while generating the answer."
    except Exception as exc:
        return f"LLM Error: {exc}"


def main():
    print("Script started")
    check_python_version()

    try:
        check_ollama_model()

        text = fetch_doc()
        print(f"Document length: {len(text)} characters")

        chunks = chunk_text(text)
        model = load_embedding_model()
        index = build_index(model, chunks)

        print("\nReady! Ask your questions. Type 'exit' to quit.\n")

        while True:
            try:
                query = input("Ask question: ").strip()
            except EOFError:
                print("No input received. Exiting...")
                break

            if not query:
                continue

            if query.lower() in ["exit", "quit"]:
                print("Exiting...")
                break

            results = search(model, query, index, chunks)
            answer = ask_llm(query, results)

            print("\nAnswer:\n" + answer + "\n")

    except Exception as exc:
        print("ERROR:", exc)


if __name__ == "__main__":
    main()
