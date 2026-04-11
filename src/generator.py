from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(query, context_docs, chat_history=None):
    context = "\n".join(context_docs)

    history_text = ""
    if chat_history:
        formatted = []
        for turn in chat_history[-5:]:
            formatted.append(f"User: {turn['user']}")
            formatted.append(f"Assistant: {turn['assistant']}")
        history_text = "\n".join(formatted)

    prompt = f"""
You are a helpful startup support assistant.

Rules:
- Answer using ONLY the provided context.
- If the answer is not in the context, say:
  "I don't know based on the available information."
- Be clear and concise.

Chat history:
{history_text}

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()