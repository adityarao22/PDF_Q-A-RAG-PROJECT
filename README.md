# 🤖 PDF Q&A RAG Assistant

An AI-powered **Retrieval-Augmented Generation (RAG)** application that lets users upload PDF documents and ask questions based on their content. The backend is a **FastAPI** service deployed on **Render**, and the frontend is a **Streamlit** chat interface.

🔗 **Live API:** https://pdf-q-a-rag-project.onrender.com
📘 **API docs (Swagger):** https://pdf-q-a-rag-project.onrender.com/docs

> ⚠️ **Free-tier note:** The API runs on Render's free plan. It sleeps after ~15 minutes of inactivity, so the first request can take 30-60 seconds. The vector index is stored on ephemeral disk and is reset on every restart or redeploy, so upload your PDFs again if the service has been asleep.

## 📌 Features

- 📄 Upload multiple PDF files
- 🔍 Ask questions based on the uploaded PDFs
- 🤖 AI-powered answers using Google Gemini
- 🧠 Retrieval-Augmented Generation (RAG)
- ⚡ Semantic search using ChromaDB
- 💬 Chat-style interface with chat history
- 🗑️ Clear chat button
- ⚠️ Error handling for timeouts, connection failures, and invalid API responses

## 🏗️ Architecture

```text
Streamlit UI (frontend)
        │  HTTP (requests)
        ▼
FastAPI backend on Render
        │
        ├── POST /upload
        │     PDFs → PyPDFLoader → text chunks (500 chars, 50 overlap)
        │     → Gemini embeddings → ChromaDB
        │
        └── POST /ask?question=...
              Question → ChromaDB retriever → relevant chunks
              → Prompt + context → Google Gemini → Answer
```

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI + Uvicorn | Backend REST API |
| Streamlit | Web user interface |
| LangChain | RAG pipeline |
| ChromaDB | Vector database |
| Google Gemini | LLM and text embeddings |
| PyPDFLoader | PDF text extraction |
| RecursiveCharacterTextSplitter | Document chunking |
| Render | Backend deployment |

## 📂 Project Structure

```text
PDF-QA-RAG-PROJECT/
├── api.py             # FastAPI backend (upload + ask endpoints)
├── embedding.py       # Gemini embeddings
├── llm.py             # Gemini LLM setup
├── app.py             # Streamlit frontend
├── requirements.txt
├── .gitignore         # includes chroma_db/
└── README.md
```

## ⚙️ How It Works

1. **Upload PDFs** through the Streamlit interface (sent to `/upload`).
2. **Extract text** using PyPDFLoader.
3. **Split documents** into smaller chunks.
4. **Generate embeddings** for each chunk with Gemini.
5. **Store vectors** in ChromaDB.
6. The user asks a **question** (sent to `/ask`).
7. The retriever finds the most relevant chunks.
8. The context and question are sent to **Google Gemini**.
9. The answer is returned and shown in the chat.

## 🚀 FastAPI Usage

The backend exposes a REST API built with FastAPI. Interactive docs are available at `/docs` (Swagger UI) and `/openapi.json`.

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Home / status message |
| GET | `/health` | Health check |
| POST | `/upload` | Upload one or more PDFs (multipart form field name: `files`) |
| POST | `/ask` | Ask a question (`question` query parameter) |

### 1. Upload PDFs

```bash
curl -X POST "https://pdf-q-a-rag-project.onrender.com/upload" \
  -F "files=@yourfile.pdf"
```

Windows (Command Prompt):

```bash
curl.exe -X POST "https://pdf-q-a-rag-project.onrender.com/upload" -F "files=@C:\path\to\yourfile.pdf"
```

To upload several PDFs, repeat the flag: `-F "files=@a.pdf" -F "files=@b.pdf"`.

**Response:**

```json
{
  "message": "PDFs processed successfully",
  "files": ["yourfile.pdf"],
  "chunks": 76
}
```

### 2. Ask a question

```bash
curl -X POST "https://pdf-q-a-rag-project.onrender.com/ask?question=What%20is%20this%20PDF%20about"
```

**Response:**

```json
{
  "question": "What is this PDF about",
  "answer": "This PDF is an operating system handout focused on file management..."
}
```

### 3. Use it from Python

```python
import requests

API_URL = "https://pdf-q-a-rag-project.onrender.com"

# Upload
with open("yourfile.pdf", "rb") as f:
    r = requests.post(
        f"{API_URL}/upload",
        files=[("files", ("yourfile.pdf", f, "application/pdf"))],
        timeout=300,
    )
print(r.json())

# Ask
r = requests.post(
    f"{API_URL}/ask",
    params={"question": "What is this PDF about?"},
    timeout=120,
)
print(r.json()["answer"])
```

> 💡 **Note:** In some FastAPI/Swagger UI versions, the `/docs` page shows the `files` field as a text box instead of a file picker. If that happens, upload with curl, Postman, or the Streamlit app. The `/ask` endpoint works fine from `/docs`.

## ▶️ How to Run

You can use the project in three ways.

### Option A: Use the deployed API (no setup)

1. Open the Streamlit app, or upload a PDF with curl (see above).
2. Ask questions through the Streamlit chat or `/ask`.
3. If the first request is slow, wait up to a minute for Render to wake up.

### Option B: Run everything locally

**1. Clone and set up**

```bash
git clone <your-github-repository-url>
cd PDF-QA-RAG-PROJECT
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

**2. Set your Google API key**

Windows (Command Prompt):

```bash
set GOOGLE_API_KEY=your_google_api_key
```

macOS / Linux:

```bash
export GOOGLE_API_KEY=your_google_api_key
```

⚠️ Never upload your API key to GitHub.

**3. Start the FastAPI backend**

```bash
uvicorn api:app --reload
```

The API runs at `http://127.0.0.1:8000`, and the docs at `http://127.0.0.1:8000/docs`.

**4. Start the Streamlit frontend** (in a second terminal, with the venv activated)

In `app.py`, set:

```python
FASTAPI_URL = "http://127.0.0.1:8000"
```

Then run:

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

### Option C: Deploy the backend on Render

1. Push the project to GitHub (make sure `chroma_db/` is in `.gitignore`).
2. On Render, create a **New → Web Service** and connect the repo.
3. Use these settings:

| Setting | Value |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn api:app --host 0.0.0.0 --port $PORT` |

4. In the **Environment** tab, add:

| Key | Value |
|---|---|
| `GOOGLE_API_KEY` | your Google API key |
| `PYTHON_VERSION` | `3.12.8` (recommended, avoids package issues on newer Python versions) |

5. Deploy. Once it is live, set `FASTAPI_URL` in `app.py` to your Render URL.

**Streamlit frontend deployment (optional):** push `app.py` and a `requirements.txt` containing `streamlit` and `requests` to GitHub, then deploy it on [Streamlit Community Cloud](https://share.streamlit.io).

## 🧩 Deployment Notes

- The backend runs on Render's free tier (512 MB RAM).
- The app originally used local HuggingFace embeddings (`all-MiniLM-L6-v2`), which pulled in PyTorch and exceeded the memory limit. Switching to **Gemini API embeddings** removed the local model and fixed the out-of-memory crash.
- If you change the embedding model, delete the old `chroma_db/` folder, because vectors from different models have different dimensions.

## 🔮 Future Improvements

- 📄 Show source PDF and page numbers with each answer
- 💾 Persistent vector storage (e.g., a hosted vector database)
- 📊 Document summarization
- 🌐 Multi-language support
- 📂 DOCX and TXT support
- 🔐 User authentication

## 🎯 Concepts Demonstrated

- Generative AI and Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Vector databases and text embeddings
- Semantic search and document chunking
- REST API design with FastAPI
- Cloud deployment and memory optimization
- LangChain and Streamlit

## 👨‍💻 Author

**Aditya Rao**

## ⭐ Conclusion

The **PDF Q&A RAG Assistant** shows how **LangChain, ChromaDB, Gemini embeddings, FastAPI, and Streamlit** can be combined and deployed to build a working document question-answering system.