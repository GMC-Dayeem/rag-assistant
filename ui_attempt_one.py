import streamlit as st
import requests
import uuid

st.set_page_config(page_title="RAG Assistant", page_icon="💬")
st.title("💬 Startup Support Assistant")

API_URL = "http://127.0.0.1:8000"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

def send_feedback(session_id, question, answer, rating):
    response = requests.post(
        f"{API_URL}/feedback",
        json={
            "session_id": session_id,
            "question": question,
            "answer": answer,
            "rating": rating
        }
    )
    return response

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            if "sources" in msg:
                with st.expander("Sources"):
                    for s in msg["sources"]:
                        st.write("- " + s)

            if "feedback_submitted" not in msg:
                msg["feedback_submitted"] = False

            if not msg["feedback_submitted"]:
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("👍 Helpful", key=f"helpful_{i}"):
                        feedback_response = send_feedback(
                            st.session_state.session_id,
                            msg.get("question", ""),
                            msg["content"],
                            "helpful"
                        )
                        if feedback_response.status_code == 200:
                            msg["feedback_submitted"] = True
                            msg["feedback_rating"] = "helpful"
                            st.rerun()
                        else:
                            st.error(f"Feedback failed: {feedback_response.text}")

                with col2:
                    if st.button("👎 Not Helpful", key=f"not_helpful_{i}"):
                        feedback_response = send_feedback(
                            st.session_state.session_id,
                            msg.get("question", ""),
                            msg["content"],
                            "not_helpful"
                        )
                        if feedback_response.status_code == 200:
                            msg["feedback_submitted"] = True
                            msg["feedback_rating"] = "not_helpful"
                            st.rerun()
                        else:
                            st.error(f"Feedback failed: {feedback_response.text}")
            else:
                if msg["feedback_rating"] == "helpful":
                    st.caption("✅ Feedback saved: Helpful")
                else:
                    st.caption("✅ Feedback saved: Not Helpful")

user_input = st.chat_input("Ask a question about the knowledge base")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        thinking = st.empty()
        thinking.markdown("Thinking...")

    response = requests.post(
        f"{API_URL}/ask",
        json={
            "query": user_input,
            "session_id": st.session_state.session_id
        }
    )

    if response.status_code == 200:
        data = response.json()
        answer = data["answer"]
        sources = data["sources"]

        assistant_message = {
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "question": user_input,
            "feedback_submitted": False
        }

        st.session_state.messages.append(assistant_message)
        st.rerun()
    else:
        st.error(f"Failed to get response from API. Status code: {response.status_code}")
        st.write(response.text)