import streamlit as st
from src.exception import CustomException
from src.logger import logging
import os
import sys
import pandas as pd
from src.database.db_prep_and_connection import DatabasePreparationAndConnection
from src.agents.agent_with_sql import SQLAgentWithSQLData
from src.agents.agent_with_csv import SQLAgentWithCSVData

st.set_page_config(page_title="SQL AI Chatbot", layout="wide")

st.title("SQL AI Agent")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Chat display
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"], avatar=msg["avatar"]):
#         st.markdown(msg["content"])

# File uploader (CSV, XLSX)
uploaded_files = st.sidebar.file_uploader(
    "📁 Upload CSV or XLSX files",
    type=["csv", "xlsx"],
    accept_multiple_files=True,
    help="Upload one or more CSV/XLSX files for processing"
)


# Dropdowns for functionality

app_functionality = st.sidebar.selectbox("App Functionality", ["Chat", "Process files"])

chat_type = st.sidebar.selectbox(
    "Chat Type",
    [
        "Chat with stored SQL-DB",
        "Chat with stored CSV-DB",
        "Chat with Uploaded CSV-DB",
    ]
)

# if st.sidebar.button("🧹 Clear Chat"):
#     st.session_state.messages = st.session_state.get("messages", [])[:0]
#     st.experimental_rerun()


# Text input





user_input = st.text_area(
    "💬 Enter your question here:",
    height=70,
    placeholder="Type your question...",
    key="chat_input_box"
)

submit_btn = st.button("🚀 Submit")

data_prep_conntection = DatabasePreparationAndConnection()
engine = data_prep_conntection.create_sqldb_from_csv()
data_prep_conntection.sql_connection_check()
data_prep_conntection.csv_connection_check(engine=engine)

# question = 'how many albums are there?'
# database = "sql"

# question = ' how many candidates have been contest the election from Lucknow PC. and what are the names od them'
question = user_input
database = "csv"

if submit_btn:

    if database=="sql":

        sql_agent_from_sql_data = SQLAgentWithSQLData()
        output = sql_agent_from_sql_data.create_sql_agent_from_sql_data(question=question)
        print(output)

    elif database=="csv":

        sql_agent_with_csv_data = SQLAgentWithCSVData()
        output = sql_agent_with_csv_data.create_sql_agent_from_csv_data(engine=engine,question=question)
        print(output)

    user_output = output

    st.text_area(
        "🤖 Agent Response",
        value=user_output,
        height=320,
        key="assistant_output_box",
        disabled=True  # Makes it read-only
    )


# File handling
# if uploaded_files:
    # response_msg = UploadFile.run_pipeline(uploaded_files, st.session_state.messages, app_functionality)
    # if response_msg:
    #     st.session_state.messages.append({"role": "assistant", "content": response_msg, "avatar": "images/openai.png"})
    # pass
# Text submit handling
# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input, "avatar": "images/AI_RT.png"})
    # response = ChatBot.respond(
    #     st.session_state.messages,
    #     user_input,
    #     chat_type,
    #     app_functionality
    # )
    # st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "images/openai.png"})

# if submit_btn and user_input.strip():
#     st.session_state.messages.append({
#         "role": "user",
#         "content": user_input,
#         "avatar": "images/AI_RT.png"
#     })

    # response = ChatBot.respond(
    #     st.session_state.messages,
    #     user_input,
    #     chat_type,
    #     app_functionality
    # )

    # st.session_state.messages.append({
    #     "role": "assistant",
    #     # "content": response,
    #     "avatar": "images/openai.png"
    # })

    # # Optionally clear input after sending
    # st.session_state.chat_input_box = ""

