# 🤖 PDF Q&A RAG Assistant

A **Retrieval-Augmented Generation (RAG)** application that allows users to ask questions based on the content of a PDF document.

The application loads a PDF, splits it into smaller chunks, converts the chunks into embeddings, stores them in **ChromaDB**, retrieves the most relevant information for a user query, and uses **Llama 3.2 through Ollama** to generate a context-aware answer.

---

## 📌 Project Overview

Traditional LLMs do not automatically know the contents of a private PDF document. This project solves that problem using **RAG (Retrieval-Augmented Generation)**.

Instead of sending the complete PDF directly to the LLM, the application:

1. Loads the PDF
2. Splits the document into chunks
3. Creates embeddings for each chunk
4. Stores embeddings in ChromaDB
5. Retrieves relevant chunks for a user question
6. Adds the retrieved context to a prompt
7. Uses an LLM to generate the final answer

---

## 🎯 Features

- 📄 Load PDF documents
- ✂️ Split PDF text into smaller chunks
- 🧠 Generate embeddings using Sentence Transformers
- 🗄️ Store embeddings in ChromaDB
- 🔍 Perform semantic similarity search
- 📚 Retrieve Top-K relevant document chunks
- 📝 Use prompt templates for context-aware answers
- 🤖 Generate answers using Ollama and Llama 3.2
- 💬 Ask questions directly from the terminal

---

# 🏗️ Architecture

```text
                    📄 PDF DOCUMENT
                           │
                           ▼
                    PyPDFLoader
                           │
                           ▼
                      PDF Text
                           │
                           ▼
              RecursiveCharacterTextSplitter
                           │
                           ▼
                      Text Chunks
                           │
                           ▼
                  Embedding Model
                           │
                           ▼
                    Vector Embeddings
                           │
                           ▼
                       ChromaDB
                           │
                           ▼
                     User Question
                           │
                           ▼
                    Query Embedding
                           │
                           ▼
                  Similarity Search
                           │
                           ▼
                Top Relevant Chunks
                           │
                           ▼
                    Prompt Template
                           │
                           ▼
                  Ollama + Llama 3.2
                           │
                           ▼
                     🤖 Final Answer
```

---

# 📁 Project Structure

```text
PDF_Q&A_RAG_PROJECT/
│
├── data/
│   └── File-management.pdf
│
├── chroma_db/
│
├── embeddings.py
├── ingest.py
├── retriever.py
├── prompt.py
├── llm.py
├── app.py
│
├── requirements.txt
└── README.md
```

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| LangChain | RAG pipeline and workflow |
| PyPDF | Reading PDF documents |
| RecursiveCharacterTextSplitter | Text chunking |
| Sentence Transformers | Creating embeddings |
| all-MiniLM-L6-v2 | Embedding model |
| ChromaDB | Vector database |
| Ollama | Running LLM locally |
| Llama 3.2 | Answer generation |

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd PDF_Q-A_RAG_PROJECT
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

## 3. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Requirements

Your `requirements.txt` should contain:

```text
langchain
langchain-community
langchain-chroma
langchain-huggingface
langchain-ollama
langchain-text-splitters
sentence-transformers
pypdf
```

---

# 🤖 Install Ollama

Install Ollama on your system and download the Llama model:

```bash
ollama pull llama3.2
```

Check the available models:

```bash
ollama list
```

---

# 📄 Add Your PDF

Place your PDF inside the `data` folder.

Example:

```text
data/
└── File-management.pdf
```

Make sure the file path in `ingest.py` matches the PDF filename.

Example:

```python
loader = PyPDFLoader("data/File-management.pdf")
```

---

# 🚀 How the Project Works

## Phase 1: Document Ingestion

Run:

```bash
python ingest.py
```

This process performs:

```text
PDF
 ↓
Load Document
 ↓
Split into Chunks
 ↓
Generate Embeddings
 ↓
Store in ChromaDB
```

### PDF Loading

The project uses `PyPDFLoader` to extract text from the PDF.

### Text Chunking

The document is divided into smaller chunks using:

```python
RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

The overlap helps preserve context between consecutive chunks.

### Embeddings

The project uses the following embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The model converts text into numerical vectors that can be compared based on semantic similarity.

### ChromaDB

The document chunks and their embeddings are stored locally in:

```text
chroma_db/
```

---

# 🔍 Phase 2: Retrieval

When a user asks a question, the application:

```text
User Question
      ↓
Query Embedding
      ↓
ChromaDB Similarity Search
      ↓
Top-K Relevant Chunks
```

The retriever is configured to return the top 3 relevant chunks.

---

# 📝 Phase 3: Prompt Augmentation

The retrieved chunks are combined with the user's question.

Example:

```text
Context:
[Relevant information from the PDF]

Question:
What is sequential access?

Answer:
```

The LLM is instructed to answer using the provided context.

---

# 🤖 Phase 4: Answer Generation

The application uses:

```text
Ollama
   +
Llama 3.2
```

The retrieved context and user question are sent to the LLM, which generates the final answer.

---

# ▶️ Running the Application

## Step 1: Create the Vector Database

```bash
python ingest.py
```

## Step 2: Run the Application

```bash
python app.py
```

You will see:

```text
🤖 PDF RAG Assistant

Type 'exit' to quit.

Ask a question:
```

Example:

```text
Ask a question: What is sequential access?
```

The application retrieves relevant information from the PDF and generates an answer.

To exit:

```text
exit
```

---

# 🔄 Complete RAG Pipeline

```text
Load
  ↓
Chunk
  ↓
Embed
  ↓
Store
  ↓
Retrieve
  ↓
Augment
  ↓
Generate
```

---

# 📂 File Explanation

## `embeddings.py`

Loads and returns the Hugging Face embedding model.

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

## `ingest.py`

Responsible for:

```text
PDF → Chunks → Embeddings → ChromaDB
```

## `retriever.py`

Loads the Chroma database and retrieves the most relevant chunks.

## `prompt.py`

Creates the prompt template containing:

- Context
- User question
- Instructions for the LLM

## `llm.py`

Loads the Llama 3.2 model through Ollama.

## `app.py`

Connects the retriever, prompt, and LLM to create the complete RAG application.

---

# 🎤 Interview Explanation

### Explain this project:

> I developed a PDF Question Answering system using Retrieval-Augmented Generation. The application loads a PDF using PyPDFLoader and splits the document into smaller chunks using RecursiveCharacterTextSplitter. I generate embeddings for the chunks using the Sentence Transformer model all-MiniLM-L6-v2 and store them in ChromaDB. When a user asks a question, the query is converted into an embedding and ChromaDB performs similarity search to retrieve the most relevant document chunks. These chunks are added as context to a prompt, and Llama 3.2 running through Ollama generates the final answer based on the retrieved information.

---

# 🎯 Key Concepts Demonstrated

- Generative AI
- Large Language Models
- Retrieval-Augmented Generation (RAG)
- Embeddings
- Vector Databases
- Semantic Search
- Similarity Search
- Prompt Engineering
- LangChain
- ChromaDB
- Ollama
- Local LLMs

---

# 🚀 Future Improvements

- Add a Streamlit web interface
- Add PDF upload functionality
- Support multiple PDFs
- Add chat history
- Add source citations with page numbers
- Add Hybrid Search
- Add reranking
- Deploy the application to the cloud

---

# 👨‍💻 Author

**Aditya Rao**

---

⭐ If you found this project useful, consider giving the repository a star!
