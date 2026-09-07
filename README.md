# 🤖 PDF Q&A RAG Assistant

An AI-powered **Retrieval-Augmented Generation (RAG)** application that
allows users to upload PDF documents and ask questions based on their
content.

## 📌 Features

-   📄 Upload multiple PDF files
-   🔍 Ask questions based on uploaded PDFs
-   🤖 AI-powered answers using Google Gemini
-   🧠 Retrieval-Augmented Generation (RAG)
-   ⚡ Fast semantic search using ChromaDB
-   💬 Chat-style interface
-   📝 Chat history
-   📄 Source PDF and page information
-   🗑️ Clear chat functionality
-   ⚠️ API rate-limit error handling

## 🏗️ Architecture

``` text
User Uploads PDFs → Extract Text → Split into Chunks → Create Embeddings
        ↓
ChromaDB Vector Database
        ↓
User Question → Retriever → Relevant Context
        ↓
Prompt + Context + Chat History
        ↓
Google Gemini LLM
        ↓
Answer + Source Pages
```

## 🛠️ Technologies Used

  Technology                       Purpose
  -------------------------------- ------------------------------
  Python                           Backend programming
  Streamlit                        Web user interface
  LangChain                        RAG pipeline
  ChromaDB                         Vector database
  Google Gemini                    Large Language Model
  PyPDFLoader                      PDF text extraction
  RecursiveCharacterTextSplitter   Document chunking
  Embeddings                       Converting text into vectors

## 📂 Project Structure

``` text
PDF-QA-RAG-PROJECT/
├── app.py
├── embedding.py
├── llm.py
├── prompt.py
├── requirements.txt
├── .gitignore
├── README.md
├── temp_pdfs/
└── chroma_db/
```

## ⚙️ How It Works

1.  **Upload PDFs** through the Streamlit interface.
2.  **Extract text** using PyPDFLoader.
3.  **Split documents** into smaller chunks.
4.  **Generate embeddings** for each chunk.
5.  **Store vectors** in ChromaDB.
6.  The user asks a **question**.
7.  The retriever finds the most relevant document chunks.
8.  The context and question are sent to **Google Gemini**.
9.  The application displays the **answer and source pages**.

## 💻 Installation

### Clone the Repository

``` bash
git clone <your-github-repository-url>
cd PDF-QA-RAG-PROJECT
```

### Create a Virtual Environment

``` bash
python -m venv venv
```

### Activate on Windows

``` bash
venv\Scripts\activate
```

### Install Dependencies

``` bash
pip install -r requirements.txt
```

## 🔑 API Key Setup

Configure your Google API key securely:

``` text
GOOGLE_API_KEY=your_google_api_key
```

⚠️ Never upload your API key to GitHub.

## ▶️ Run the Application

``` bash
streamlit run app.py
```

The application usually opens at:

``` text
http://localhost:8501
```

<<<<<<< HEAD
## ⚠️ Error Handling

The application handles:

-   No PDF processed
-   API rate limits
-   Gemini quota exceeded
-   Vector database errors
-   Invalid LLM responses

## 🔮 Future Improvements

-   📑 PDF preview
-   🔎 Advanced semantic search
-   📊 Document summarization
-   🌐 Multi-language support
-   🎤 Voice questions
-   📂 DOCX and TXT support
-   🔐 User authentication
-   ☁️ Cloud deployment

## 🎯 Concepts Demonstrated

-   Generative AI
-   Large Language Models (LLMs)
-   Retrieval-Augmented Generation (RAG)
-   Vector Databases
-   Text Embeddings
-   Semantic Search
-   Prompt Engineering
-   Document Chunking
-   Context Retrieval
-   LangChain
-   Streamlit

## 👨‍💻 Author
=======
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
>>>>>>> cf1935866b3ab3287877558a439a921083249140

**Aditya Rao**

AI / Machine Learning Enthusiast

## ⭐ Conclusion

The **PDF Q&A RAG Assistant** demonstrates how **LangChain, ChromaDB,
embeddings, Streamlit, and Google Gemini** can be combined to build an
intelligent document question-answering system.
