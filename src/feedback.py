import json
import os

def save_feedback(session_id, question, answer, rating):
    feedback_entry = {
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "rating": rating
    }

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "feedback.json")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    data = []
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except (json.JSONDecodeError, OSError):
            data = []

    data.append(feedback_entry)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)