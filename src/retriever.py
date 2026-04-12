import json
from sentence_transformers import SentenceTransformer
# import chromadb
import numpy as np
import os



# # Load model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Create DB
# client = chromadb.Client()
# try:
#     collection = client.get_collection("docs")
# except:
#     collection = client.create_collection("docs")
# # Load documents

# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# file_path = os.path.join(base_dir, "data", "docs.json")

# with open(file_path, "r", encoding="utf-8") as f:
#     docs = json.load(f)


# # Add documents to DB
# if collection.count() == 0:
#     embeddings = model.encode(docs).tolist()
#     collection.add(
#         documents=docs,
#         embeddings=embeddings,
#         ids=[str(i) for i in range(len(docs))]
#     )

# def retrieve(query: str, k: int = 3):
#     query_embedding = model.encode([query]).tolist()
#     results = collection.query(query_embeddings=query_embedding, n_results=k)
#     docs = results.get("documents", [[]])[0]
    
#     return docs if docs else ["No relevant documents found."]


model = SentenceTransformer("all-MiniLM-L6-v2")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, "data", "docs.json")

with open(file_path, "r", encoding="utf-8") as f:
    docs = json.load(f)

doc_embeddings = model.encode(docs)

def retrieve(query: str, k: int = 3):
    query_embedding = model.encode([query])[0]

    doc_norms = np.linalg.norm(doc_embeddings, axis=1)
    query_norm = np.linalg.norm(query_embedding)

    similarities = np.dot(doc_embeddings, query_embedding) / (doc_norms * query_norm + 1e-10)
    top_indices = np.argsort(similarities)[-k:][::-1]

    return [docs[i] for i in top_indices]