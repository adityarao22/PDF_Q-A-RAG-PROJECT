from fastapi import FastAPI, UploadFile, File
from typing import List
import os
import shutil

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from embedding import get_embeddings
from llm import get_llm


app = FastAPI(
    title="PDF Q&A RAG API",
    description="PDF Question Answering using ChromaDB and Gemini",
    version="1.0"
)


# ---------------- LOAD MODELS ----------------


llm = get_llm()


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {
        "message": "PDF Q&A API is running"
    }


# ---------------- HEALTH ----------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ---------------- UPLOAD PDF ----------------

@app.post("/upload")
async def upload_pdfs(
    files: List[UploadFile] = File(...)
):
    embeddings = get_embeddings()
    os.makedirs("temp_pdfs", exist_ok=True)

    all_documents = []

    for file in files:

        file_path = os.path.join(
            "temp_pdfs",
            file.filename
        )

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        loader = PyPDFLoader(file_path)

        documents = loader.load()

        all_documents.extend(documents)


    # Split PDF text

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(
        all_documents
    )


    # ChromaDB

    vectorstore = Chroma(
        collection_name="rag_documents",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )

    vectorstore.add_documents(chunks)


    return {
        "message": "PDFs processed successfully",
        "files": [file.filename for file in files],
        "chunks": len(chunks)
    }


# ---------------- ASK QUESTION ----------------

@app.post("/ask")
def ask_question(question: str):
    embeddings = get_embeddings()

    # Load ChromaDB

    vectorstore = Chroma(
        collection_name="rag_documents",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )


    # Retriever

    current_retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 4
        }
    )


    # Retrieve documents

    documents = current_retriever.invoke(
        question
    )


    # Create context

    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )


    # Prompt

    prompt = f"""
You are a PDF question-answering assistant.

Use ONLY the information from the PDF content below.

PDF CONTENT:
{context}

QUESTION:
{question}

Instructions:

- Answer the question directly.
- Give a short and clear answer.
- Use only relevant information from the PDF.
- Do not invent information.
- Do not mention the context or retrieval process.
- Keep the answer simple for a college student.

Answer:
"""


    # Gemini

    response = llm.invoke(
        prompt
    )


    # Get answer

    answer = response.content


    # Handle string response

    if isinstance(answer, str):

        final_answer = answer


    # Handle list response

    elif isinstance(answer, list):

        final_answer = ""

        for item in answer:

            if isinstance(item, dict):

                if item.get("text"):

                    final_answer += item["text"]

            elif hasattr(item, "text"):

                final_answer += item.text


    else:

        final_answer = str(answer)


    # Safety check

    if not final_answer:

        final_answer = (
            "I could not generate an answer."
        )


    return {
        "question": question,
        "answer": final_answer
    }