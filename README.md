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

**Aditya Rao**

AI / Machine Learning Enthusiast

## ⭐ Conclusion

The **PDF Q&A RAG Assistant** demonstrates how **LangChain, ChromaDB,
embeddings, Streamlit, and Google Gemini** can be combined to build an
intelligent document question-answering system.
