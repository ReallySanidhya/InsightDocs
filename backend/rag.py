from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import requests

# Local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")




def chunk_text(
    pages: List[Dict],
    chunk_size: int = 1000,
    overlap: int = 200
) -> List[Dict]:
    chunks = []
    chunk_id = 0

    for page in pages:
        text = page["text"]
        if not text.strip():
            continue

        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(
                    {
                        "text": chunk,
                        "source": page["source"],
                        "page_number": page["page_number"],
                        "chunk_id": chunk_id,
                    }
                )
                chunk_id += 1

            start += chunk_size - overlap

    return chunks


def create_embeddings(chunks: List[Dict]) -> Tuple[np.ndarray, List[Dict]]:
    texts = [chunk["text"] for chunk in chunks]
    vectors = model.encode(texts, convert_to_numpy=True)
    faiss.normalize_L2(vectors)
    return vectors, chunks


def build_faiss_index(vectors: np.ndarray) -> faiss.IndexFlatIP:
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)
    return index


def search_chunks(
    question: str,
    index: faiss.IndexFlatIP,
    chunks: List[Dict],
    top_k: int = 3
) -> List[Dict]:
    q_vector = model.encode([question], convert_to_numpy=True)
    faiss.normalize_L2(q_vector)

    scores, ids = index.search(q_vector, top_k)

    results = []
    for idx, score in zip(ids[0], scores[0]):
        if idx == -1:
            continue
        result = chunks[idx].copy()
        result["score"] = float(score)
        results.append(result)

    return results


def build_context(results: List[Dict]) -> str:
    parts = []
    for r in results:
        parts.append(
            f"Source: {r['source']} | Page: {r['page_number']}\n{r['text']}"
        )
    return "\n\n---\n\n".join(parts)



def generate_answer(question: str, results: List[Dict]) -> str:
    context = build_context(results)

    prompt = f"""
You are a helpful research assistant.

Answer the question using ONLY the context below.
If the answer is not in the context, say: "I could not find that in the documents."

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"]