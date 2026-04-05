# InsightDocs
<img width="1658" height="952" alt="image" src="https://github.com/user-attachments/assets/109820e9-0356-4216-8c36-40a33743853b" />

I built an AI research assistant using a RAG pipeline that allows users to upload PDFs and query them. The system extracts and chunks text, converts it into embeddings, and uses FAISS for semantic retrieval. The retrieved context is then passed to a local LLM to generate grounded answers with source citations, reducing hallucination and improving reliability.

Here, I chose Streamlit for rapid UI development, FastAPI for efficient backend APIs, SentenceTransformers for semantic embeddings, FAISS for fast vector search, and Ollama with Llama3 for local LLM inference. This combination allowed me to build a complete RAG system that is efficient, cost-free, and scalable.

Full system flow that I designed before actual implementation:

<img width="674" height="482" alt="image" src="https://github.com/user-attachments/assets/5e42ad74-630e-41df-a954-bb7e64a8c70e" />


Old layout:

<img width="1677" height="837" alt="image" src="https://github.com/user-attachments/assets/82b5371d-963b-48a0-9cbf-76dc9eaa0b83" />

<img width="845" height="540" alt="image" src="https://github.com/user-attachments/assets/fbdff1aa-3495-4ff3-ba88-450ba8147a5a" />

