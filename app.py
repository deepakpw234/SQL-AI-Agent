from src.exception import CustomException
from src.logger import logging



import streamlit as st
from utils.upload_file import UploadFile
from utils.chatbot import ChatBot

# Session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

st.set_page_config(page_title="Q&A and RAG with SQL and Tabular Data", layout="wide")

# Title and tabs
st.title("Q&A and RAG with SQL and Tabular Data")
tab1, = st.tabs(["Q&A-and-RAG-with-SQL-and-TabularData"])

with tab1:
    # First ROW: Chatbot display
    st.subheader("Chat Interface")
    for message in st.session_state.chat_history:
        with st.chat_message("user" if message["role"] == "user" else "assistant"):
            st.markdown(message["content"])

    # SECOND ROW: Input box
    st.subheader("User Input")
    st.session_state.input_text = st.text_area(
        "Enter text and press enter, or upload CSV/XLSX files",
        value=st.session_state.input_text,
        height=100,
        key="input_area"
    )

    # THIRD ROW: Buttons and Dropdowns
    col1, col2, col3, col4, col5 = st.columns([1, 1.5, 2, 3, 1])
    with col1:
        if st.button("Submit text"):
            if st.session_state.input_text.strip():
                input_text, chat_history = ChatBot.respond(
                    st.session_state.chat_history,
                    st.session_state.input_text,
                    st.session_state.get("chat_type", "Q&A with stored SQL-DB"),
                    st.session_state.get("app_functionality", "Chat")
                )
                st.session_state.input_text = input_text
                st.session_state.chat_history = chat_history

    with col2:
        uploaded_files = st.file_uploader("Upload CSV or XLSX files", type=['csv', 'xlsx'], accept_multiple_files=True)
        if uploaded_files:
            input_text, chat_history = UploadFile.run_pipeline(
                uploaded_files,
                st.session_state.chat_history,
                st.session_state.get("app_functionality", "Chat")
            )
            st.session_state.input_text = input_text
            st.session_state.chat_history = chat_history

    with col3:
        st.session_state.app_functionality = st.selectbox(
            "App functionality",
            options=["Chat", "Process files"],
            index=0 if st.session_state.get("app_functionality", "Chat") == "Chat" else 1
        )

    with col4:
        st.session_state.chat_type = st.selectbox(
            "Chat type",
            options=[
                "Q&A with stored SQL-DB",
                "Q&A with stored CSV/XLSX SQL-DB",
                "RAG with stored CSV/XLSX ChromaDB",
                "Q&A with Uploaded CSV/XLSX SQL-DB"
            ],
            index=[
                "Q&A with stored SQL-DB",
                "Q&A with stored CSV/XLSX SQL-DB",
                "RAG with stored CSV/XLSX ChromaDB",
                "Q&A with Uploaded CSV/XLSX SQL-DB"
            ].index(st.session_state.get("chat_type", "Q&A with stored SQL-DB"))
        )

    with col5:
        if st.button("Clear"):
            st.session_state.input_text = ""
            st.session_state.chat_history = []
