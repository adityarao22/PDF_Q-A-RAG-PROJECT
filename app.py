import streamlit as st
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from embedding import get_embeddings
from prompt import prompt
from llm import get_llm

st.set_page_config(
    page_title="PDF Q&A RAG Assistant",
    page_icon="🤖"
)
st.title("🤖 PDF Q&A RAG Assistant")

# ---------------- LOAD MODELS ----------------

@st.cache_resource
def load_embeddings():
    return get_embeddings()

@st.cache_resource
def load_llm():
    return get_llm()

embeddings = load_embeddings()
llm = load_llm()

# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("📄 Upload PDFs")
    uploaded_files = st.file_uploader(
        "Upload one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )
    process_button = st.button("Process PDFs")
    st.divider()
    st.subheader("⚙️ Controls")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- PROCESS PDFs ----------------

if process_button and uploaded_files:
    with st.spinner("Processing PDFs..."):
        # Initialize document list
        all_documents = []
        # Create temporary folder
        os.makedirs("temp_pdfs", exist_ok=True)
        # Process uploaded PDFs
        for uploaded_file in uploaded_files:
            file_path = os.path.join(
                "temp_pdfs",
                uploaded_file.name
            )
            # Save PDF
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Load PDF
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            # Add documents
            all_documents.extend(documents)
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = text_splitter.split_documents(all_documents)
        # Create vector database
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name="rag_documents"
        )
        # Save vectorstore in memory
        st.session_state.vectorstore = vectorstore
        # Clear previous chat
        st.session_state.messages = []
        st.success(
            f"✅ Successfully processed {len(uploaded_files)} PDF(s)!"
        )


def get_retriever():
    if "vectorstore" not in st.session_state:
        return None
    return st.session_state.vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

def format_docs(docs):
    return "\n\n".join(
        doc.page_content for doc in docs
    )

def extract_text(content):
    # If response is already a string
    if isinstance(content, str):
        return content
    # If response is a list of blocks
    if isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    texts.append(item.get("text", ""))
            # Handle object-based content blocks
            elif hasattr(item, "text"):
                texts.append(item.text)
        return "".join(texts)
    return str(content)

def ask_question(question):
    retriever = get_retriever()
    if retriever is None:
        return "⚠️ Please upload and process PDF files first.", []
    # Retrieve relevant documents
    docs = retriever.invoke(question)
    # Create context
    context = format_docs(docs)
    # Get source pages
    sources = []
    for doc in docs:
        page = doc.metadata.get("page", None)
        source = doc.metadata.get("source", "Unknown")
        if page is not None:
            sources.append(
                f"{os.path.basename(source)} - Page {page + 1}"
            )
    # Remove duplicates
    sources = list(set(sources))
    # Create chat history
    chat_history = ""
    for message in st.session_state.messages:
        chat_history += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )
    # Create prompt
    messages = prompt.invoke({
        "context": context,
        "question": question,
        "chat_history": chat_history
    })

    try:
      response = llm.invoke(messages)
      answer = extract_text(response.content)
      return answer, sources
    except Exception as e:  
        error_message = str(e) 
        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            return (
                "⚠️ Gemini API rate limit reached. Please wait a few seconds and try again.",
                []
            )
        return (
            f"⚠️ Error while generating answer: {error_message}",
            []
        )

# ---------------- DISPLAY CHAT HISTORY ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# ---------------- USER INPUT ----------------

question = st.chat_input(
    "Ask a question about your PDFs..."
)
if question:
    with st.chat_message("user"):
        st.write(question)
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    with st.chat_message("assistant"):
        with st.spinner("Searching PDFs..."):
            answer, sources = ask_question(question)
        st.write(answer)
        if sources:
            st.caption(
                "📄 Sources: " +
                " | ".join(sources)
            )
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })