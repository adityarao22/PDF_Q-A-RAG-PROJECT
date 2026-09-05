from langchain_chroma import Chroma
from embedding import get_embeddings
# Load the same embedding model
embeddings = get_embeddings()
# Load existing Chroma database
vectorstore = Chroma(
    collection_name="rag_documents",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
# Create retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)