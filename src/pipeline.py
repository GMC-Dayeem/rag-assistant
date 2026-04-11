from src.retriever import retrieve
from src.generator import generate_answer
from src.memory import get_history, add_turn

def ask(query, session_id="default", k=3):
    docs = retrieve(query, k=k)
    history = get_history(session_id)
    answer = generate_answer(query, docs, history)

    add_turn(session_id, query, answer)

    return {
        "query": query,
        "answer": answer,
        "sources": docs,
        "session_id": session_id
    }