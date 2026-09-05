from retriever import retriever
from prompt import prompt
from llm import get_llm
# Load LLM
llm = get_llm()
def format_docs(docs):
    """Combine retrieved documents into one context."""
    return "\n\n".join(doc.page_content for doc in docs)
def ask_question(question):
    # 1. Retrieve relevant chunks
    docs = retriever.invoke(question)
    # 2. Convert chunks into context
    context = format_docs(docs)
    # 3. Create prompt
    messages = prompt.invoke({
        "context": context,
        "question": question
    })
    # 4. Generate answer
    response = llm.invoke(messages)
    return response.content
if __name__ == "__main__":
    print("🤖 PDF RAG Assistant")
    print("Type 'exit' to quit.\n")
    while True:
        question = input("Ask a question: ")
        if question.lower() == "exit":
            print("Goodbye! 👋")
            break
        answer = ask_question(question)
        print("\nAnswer:")
        print(answer)
        print("\n" + "-" * 50)