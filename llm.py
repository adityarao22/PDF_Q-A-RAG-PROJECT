from langchain_ollama import ChatOllama
def get_llm():
    return ChatOllama(
        model="llama3.2",
        temperature=0
    )