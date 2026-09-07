from langchain_core.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_template("""
You are a helpful PDF Question Answering Assistant.

Answer the user's question using the provided document context.

If the answer is not available in the context, say:
"I don't know based on the provided documents."
Previous Conversation:
{chat_history}
Document Context:
{context}
Current Question:
{question}
Answer:
""")