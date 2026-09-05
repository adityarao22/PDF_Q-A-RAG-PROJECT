from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from embedding import get_embeddings
# 1. Load PDF
loader = PyPDFLoader("data/File-management.pdf")
documents = loader.load()
print(f"Total pages: {len(documents)}")
# 2. Create chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)
print(f"Total chunks: {len(chunks)}")
# 3. Load embedding model
embeddings = get_embeddings()
# 4. Store chunks in Chroma
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="rag_documents",
    persist_directory="./chroma_db"
)
print("✅ PDF successfully stored in Chroma DB!")