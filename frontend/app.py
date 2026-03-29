import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="InsightDocs", layout="wide")

st.markdown(
    """
    <style>
    /* Main app background */
    .stApp {
        background-color: #BAF3F7;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #BAF3F7;
    }

    /* Sidebar text color */
    section[data-testid="stSidebar"] * {
        color: black;
    }  

    </style>
    """,
    unsafe_allow_html=True
)
st.title("📄 InsightDocs")
st.caption("Ask questions from your uploaded PDFs")

# Sidebar for upload
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Process PDF"):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(f"{BACKEND_URL}/upload-pdf", files=files)

            if response.status_code == 200:
                st.success("✅ PDF processed successfully yaay!")
            else:
                st.error("❌ Error processing PDF oops")

# Main chat area
st.subheader("Ask Questions")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input("Enter your question")

if st.button("Get Answer"):
    if question:
        response = requests.get(
            f"{BACKEND_URL}/search",
            params={"question": question}
        )

        if response.status_code == 200:
            data = response.json()

            # Save chat history
            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": data["answer"],
                    "sources": data["retrieved_chunks"],
                }
            )
        else:
            st.error("Error getting answer")

# Display chat history
for chat in reversed(st.session_state.chat_history):
    st.markdown("### ❓ " + chat["question"])
    st.markdown("**Answer:**")
    st.write(chat["answer"])

    with st.expander("📚 Sources"):
        for chunk in chat["sources"]:
            st.markdown(f"""
**{chunk['source']} (Page {chunk['page_number']})**

{chunk['text'][:300]}...
---
""")
            
st.markdown(
    """
    <hr>
    <div style='text-align: center; color: black; font-size: 20px;'>
        Made by Sanidhya
    </div>
    """,
    unsafe_allow_html=True
)