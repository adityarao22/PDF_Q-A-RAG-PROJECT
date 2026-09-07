import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
def get_llm():

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=st.secrets["GOOGLE_API_KEY"],
        temperature=0
    )