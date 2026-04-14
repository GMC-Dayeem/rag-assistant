# 💬 Website-Aware AI Support Assistant (RAG)

An AI-powered assistant that analyzes website content and answers questions about policies, pricing, and support information using Retrieval-Augmented Generation (RAG).

🔗 **Live Demo:** https://rag-assistant-gmcd.streamlit.app/



## 🚀 Features

- 🌐 **Website-Aware Q&A**  
  Enter any website URL and ask questions about its content

- 🧠 **Semantic Search (RAG Pipeline)**  
  Uses sentence embeddings and similarity search to retrieve relevant information

- 🤖 **LLM-Powered Responses**  
  Generates natural language answers grounded in retrieved content

- 💬 **Chat Interface with Memory**  
  Maintains session-based conversation flow

- 📊 **Source Attribution**  
  Shows relevant text chunks used to generate answers

- 👍 **Feedback System**  
  Users can rate responses to simulate real-world model improvement


## 🧠 How It Works

1. User enters a **website URL** and a **question**
2. The app **scrapes website content**
3. Text is **cleaned and split into chunks**
4. Chunks are converted into **embeddings**
5. The system retrieves the most relevant chunks using **cosine similarity**
6. An LLM generates an answer based on retrieved context
7. The app displays the **answer + sources**



## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)  
- **LLM:** OpenAI API  
- **Retrieval:** Cosine similarity (NumPy)  
- **Web Scraping:** Firecrawl API  



## 💡 Example Questions
- What is the refund policy of this website?
- Does this company offer free shipping?
- What are the pricing plans?
- How do I contact support?

## ⚠️ Notes
- Works best on public, text-based web pages
- Some websites may block scraping or require JavaScript rendering
- Responses are based only on retrieved content (no hallucination intended)

## 🔮 Future Improvements
- Multi-page website crawling
- Better content filtering (policies, pricing, support)
- Database-backed feedback tracking
- Playwright support for dynamic websites
- Deployment optimization and caching