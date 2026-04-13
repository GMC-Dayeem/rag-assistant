import streamlit as st
# import requests
import uuid
from src.pipeline import ask
from src.feedback import save_feedback
from src.web_pipeline import ask_website

st.set_page_config(
    page_title="Website Support AI Assistant",
    page_icon="💬",
    layout="centered"
)

# API_URL = "http://127.0.0.1:8000"

# ---------- Session State ----------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Helpers ----------
# def send_feedback(session_id, question, answer, rating):
#     return requests.post(
#         f"{API_URL}/feedback",
#         json={
#             "session_id": session_id,
#             "question": question,
#             "answer": answer,
#             "rating": rating
#         },
#         timeout=30
#     )

def send_feedback(session_id, question, answer, rating):
    save_feedback(session_id, question, answer, rating)
    return True

def clear_chat():
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.header("Session")
    st.caption(f"ID: {st.session_state.session_id[:8]}")
    if st.button("Clear chat", use_container_width=True):
        clear_chat()
        st.rerun()

    
    st.divider()
    st.markdown("## About")
    st.caption(
    "An AI assistant that analyzes website content to answer questions about policies, pricing, and support information. Uses semantic search, LLMs, and retrieval-augmented generation (RAG) with source-based responses."
    )
    st.info("⚡ Powered by semantic search + LLM (RAG system)")

# ---------- Header ----------
st.markdown("""
<h1 style='text-align: center;'>💬 Website Support AI Assistant</h1>

<p style='text-align: center; color: gray; max-width: 700px; margin: auto;'>
This is an AI-powered assistant built using Retrieval-Augmented Generation (RAG). 
It can analyze website content and answer questions about policies, pricing, and support information in real time.
</p>
""", unsafe_allow_html=True)

st.markdown("### 💡 Try asking:")

st.markdown("""
💡 Try asking:
What is the refund policy of this website?
Does this company offer free shipping?
What are the pricing plans?
How can I cancel a subscription?
""")


# ---------- Chat History ----------
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            if msg.get("sources"):
                with st.expander("Sources"):
                    for s in msg["sources"]:
                        st.write("- " + s)

            if "feedback_submitted" not in msg:
                msg["feedback_submitted"] = False

            if msg["feedback_submitted"]:
                display_rating = (
                    "Helpful" if msg.get("feedback_rating") == "helpful" else "Not Helpful"
                )
                st.caption(f"✅ Feedback saved: {display_rating}")
            else:
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("👍 Helpful", key=f"helpful_{i}", use_container_width=True):
                        # feedback_response = send_feedback(
                        #     st.session_state.session_id,
                        #     msg.get("question", ""),
                        #     msg["content"],
                        #     "helpful"
                        # )
                        # if feedback_response.status_code == 200:
                        send_feedback(
                            st.session_state.session_id,
                            msg.get("question", ""),
                            msg["content"],
                            "helpful"
                        )
                        msg["feedback_submitted"] = True
                        msg["feedback_rating"] = "helpful"
                        st.rerun()
                        # else:
                        #     st.error(f"Feedback failed: {feedback_response.text}")

                with col2:
                    if st.button("👎 Not Helpful", key=f"not_helpful_{i}", use_container_width=True):
                        # feedback_response = send_feedback(
                        #     st.session_state.session_id,
                        #     msg.get("question", ""),
                        #     msg["content"],
                        #     "not_helpful"
                        # )
                        # if feedback_response.status_code == 200:
                        #     msg["feedback_submitted"] = True
                        #     msg["feedback_rating"] = "not_helpful"
                        #     st.rerun()
                        # else:
                        #     st.error(f"Feedback failed: {feedback_response.text}")
                        send_feedback(
                            st.session_state.session_id,
                            msg.get("question", ""),
                            msg["content"],
                            "not_helpful"
                        )
                        msg["feedback_submitted"] = True
                        msg["feedback_rating"] = "not_helpful"
                        st.rerun()

# ---------- User Input ----------
st.info("🌐 Enter a website URL and ask questions about its policies, pricing, or support.")
website_url = st.text_input("Website URL", placeholder="https://example.com")
user_input = st.chat_input("Ask a question about this website")
# user_input = st.chat_input("Ask a question about the knowledge base")

# if user_input:
#     # show user message immediately
#     st.session_state.messages.append({
#         "role": "user",
#         "content": user_input
#     })

#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # nicer loading state
#     with st.chat_message("assistant"):
#         with st.spinner("Searching the knowledge base and generating a response..."):
#             try:
#                 # response = requests.post(
#                 #     f"{API_URL}/ask",
#                 #     json={
#                 #         "query": user_input,
#                 #         "session_id": st.session_state.session_id
#                 #     },
#                 #     timeout=60
#                 result = ask(user_input, session_id=st.session_state.session_id)
#                 answer = result["answer"]
#                 sources = result["sources"]
                
#             # except requests.RequestException as e:
#             except Exception as e:
#                 # st.error(f"Request failed: {e}")
#                 st.error(f"Failed to generate response: {e}")
#                 st.stop()

#     # if response.status_code == 200:
#     #     data = response.json()
#     #     answer = data["answer"]
#     #     sources = data["sources"]

#     assistant_message = {
#         "role": "assistant",
#         "content": answer,
#         "sources": sources,
#         "question": user_input,
#         "feedback_submitted": False
#     }

#     st.session_state.messages.append(assistant_message)
#     st.rerun()
#     # else:
#     #     st.error(f"Failed to get response from API. Status code: {response.status_code}")
#     #     st.write(response.text)

if user_input:
    if not website_url:
        st.error("Please enter a website URL first.")
        st.stop()

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Reading the website and generating a response..."):
            try:
                result = ask_website(website_url, user_input)
                answer = result["answer"]
                sources = result["sources"]
            except Exception as e:
                st.error(f"Failed to analyze website: {e}")
                st.stop()

    assistant_message = {
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "question": user_input,
        "feedback_submitted": False
    }

    st.session_state.messages.append(assistant_message)
    st.rerun()