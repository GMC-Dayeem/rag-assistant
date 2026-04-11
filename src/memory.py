chat_sessions = {}

def get_history(session_id: str):
    return chat_sessions.get(session_id, [])

def add_turn(session_id: str, user_message: str, assistant_message: str):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    chat_sessions[session_id].append({
        "user": user_message,
        "assistant": assistant_message
    })