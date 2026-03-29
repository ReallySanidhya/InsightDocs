from fastapi import FastAPI, UploadFile, File
from backend.pdf_utils import extract_pdf_text
from backend.rag import (
    chunk_text,
    create_embeddings,
    build_faiss_index,
    search_chunks,
    generate_answer,
)
import os
import shutil

app = FastAPI()

stored_chunks = []
faiss_index = None


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global stored_chunks, faiss_index

    upload_dir = "data"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_pdf_text(file_path)
    chunks = chunk_text(pages)

    if not chunks:
        return {
            "filename": file.filename,
            "pages_extracted": len(pages),
            "chunks_created": 0,
            "message": "No text chunks found.",
        }

    vectors, metadata = create_embeddings(chunks)
    faiss_index = build_faiss_index(vectors)
    stored_chunks = metadata

    return {
        "filename": file.filename,
        "pages_extracted": len(pages),
        "chunks_created": len(chunks),
        "sample_chunks": chunks[:2],
        "message": "Embeddings created and FAISS index built.",
    }


@app.get("/search")
async def search(question: str):
    global stored_chunks, faiss_index

    if faiss_index is None or not stored_chunks:
        return {"error": "No document has been uploaded and indexed yet."}

    results = search_chunks(question, faiss_index, stored_chunks, top_k=3)
    answer = generate_answer(question, results)

    return {
        "question": question,
        "answer": answer,
        "retrieved_chunks": results,
    }