import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(chunks):
    embeddings = model.encode(chunks)
    return chunks, embeddings

def retrieve_from_chunks(query: str, chunks, embeddings, k: int = 3):
    query_embedding = model.encode([query])[0]

    emb_norms = np.linalg.norm(embeddings, axis=1)
    q_norm = np.linalg.norm(query_embedding)

    similarities = np.dot(embeddings, query_embedding) / (emb_norms * q_norm + 1e-10)
    top_indices = np.argsort(similarities)[-k:][::-1]

    return [chunks[i] for i in top_indices]