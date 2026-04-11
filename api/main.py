from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline import ask
from src.feedback import save_feedback

app = FastAPI()

class AskRequest(BaseModel):
    query: str
    session_id: str = "default"

@app.get("/")
def home():
    return {"message": "RAG Assistant is running"}

@app.post("/ask")
def ask_question(request: AskRequest):
    result = ask(request.query, session_id=request.session_id)
    return {
        "question": result["query"],
        "answer": result["answer"],
        "sources": result["sources"],
        "session_id": result["session_id"]
    }

class FeedbackRequest(BaseModel):
    session_id: str
    question: str
    answer: str
    rating: str

@app.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    save_feedback(
        request.session_id,
        request.question,
        request.answer,
        request.rating
    )
    return {"message": "Feedback saved"}