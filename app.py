import streamlit as st
import requests


st.set_page_config(
    page_title="PDF Q&A RAG Assistant",
    page_icon="🤖"
)

st.title("🤖 PDF Q&A RAG Assistant")


FASTAPI_URL = "http://127.0.0.1:8000"


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.header("📄 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process PDFs"):
        if uploaded_files:
            files = [
                (
                    "files",
                    (
                        file.name,
                        file.getvalue(),
                        "application/pdf"
                    )
                )
                for file in uploaded_files
            ]

            response = requests.post(
                f"{FASTAPI_URL}/upload",
                files=files
            )

            if response.status_code == 200:
                data = response.json()
                st.success(
                    f"✅ Processed {data['chunks']} chunks"
                )
            else:
                st.error(
                    f"❌ Upload failed: {response.text}"
                )
        else:
            st.warning("Please select a PDF first.")


# =====================================================
# CHAT HISTORY
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# =====================================================
# ASK QUESTION
# =====================================================

question = st.chat_input(
    "Ask a question about your PDFs..."
)


if question:

    # ---------------- USER ----------------

    with st.chat_message("user"):

        st.write(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # ---------------- ASSISTANT ----------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching PDFs..."
        ):

            try:

                response = requests.post(
                    f"{FASTAPI_URL}/ask",
                    params={
                        "question": question
                    },
                    timeout=120
                )

                # Check HTTP status
                if response.status_code != 200:

                    st.error(
                        f"❌ FastAPI returned "
                        f"status {response.status_code}"
                    )

                    st.code(response.text)

                    answer = (
                        "Unable to get an answer "
                        "from the backend."
                    )

                else:

                    # Convert response to JSON
                    data = response.json()

                    # Debug safety check
                    if not isinstance(data, dict):

                        st.error(
                            "❌ FastAPI returned an "
                            "unexpected response."
                        )

                        st.code(
                            str(data)
                        )

                        answer = (
                            "Invalid response from FastAPI."
                        )

                    elif "answer" not in data:

                        st.error(
                            "❌ 'answer' field is missing "
                            "from FastAPI response."
                        )

                        st.json(data)

                        answer = (
                            "FastAPI did not return an answer."
                        )

                    else:

                        answer = data["answer"]

            except requests.exceptions.ConnectionError:

                answer = (
                    "⚠️ Cannot connect to FastAPI. "
                    "Please make sure FastAPI is running."
                )

            except requests.exceptions.Timeout:

                answer = (
                    "⚠️ FastAPI request timed out. "
                    "Please try again."
                )

            except requests.exceptions.JSONDecodeError:

                answer = (
                    "⚠️ FastAPI returned an invalid response."
                )

                st.code(response.text)

            except Exception as e:

                answer = f"⚠️ Error: {str(e)}"


        st.write(answer)


    # Save assistant message

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )