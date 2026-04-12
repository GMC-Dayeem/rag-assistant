from src.web_loader import scrape_website
from src.chunker import chunk_text
from src.web_retriever import build_index, retrieve_from_chunks
from src.generator import generate_answer

def ask_website(url: str, query: str):
    text = scrape_website(url)
    chunks = chunk_text(text)
    indexed_chunks, embeddings = build_index(chunks)
    top_chunks = retrieve_from_chunks(query, indexed_chunks, embeddings, k=3)
    answer = generate_answer(query, top_chunks, chat_history=None)

    return {
        "answer": answer,
        "sources": top_chunks
    }