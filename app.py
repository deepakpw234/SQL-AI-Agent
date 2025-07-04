import streamlit as st
from src.exception import CustomException
from src.logger import logging
import os
import sys
import pandas as pd
from src.database.db_prep_and_connection import DatabasePreparationAndConnection
from src.database.upload_file_db_preparation import UploadedFileDatabasePreparation
from src.agents.agent_with_sql import SQLAgentWithSQLData
from src.agents.agent_with_csv import SQLAgentWithCSVData
from src.agents.agent_with_upload_csv import SQLAgentWithUploadCSVData
from src.pipeline.audio_query import AudioQuery

st.set_page_config(page_title="SQL AI Chatbot", layout="wide")

st.title("SQL AI Agent")


# File uploader (CSV, XLSX)
uploaded_files = st.sidebar.file_uploader(
    "📁 Upload CSV or XLSX files",
    type=["csv", "xlsx"],
    help="Upload one or more CSV/XLSX files for processing"
)


uploaded_engine = None
if uploaded_files:
    uploaded_file_dir = os.path.join(os.getcwd(),'artifacts','upload_data')
    os.makedirs(uploaded_file_dir,exist_ok=True)
    uploaded_file_path = os.path.join(uploaded_file_dir,uploaded_files.name)
    with open(uploaded_file_path, "wb") as f:
        f.write(uploaded_files.getbuffer())

    upload_file_db_prep = UploadedFileDatabasePreparation()
    uploaded_engine = upload_file_db_prep.create_sqldb_from_csv()
    upload_file_db_prep.csv_connection_check(engine=uploaded_engine)
    


chat_type = st.sidebar.selectbox(
    "Chat Type",
    [
        "Chat with stored SQL-DB",
        "Chat with stored CSV-DB",
        "Chat with Uploaded CSV-DB",
    ]
)

query_option = st.sidebar.radio(label='Query Format',options=['Text','Audio'])


if st.sidebar.button("Clear Uploaded DB"):
    uploaded_db_path = r"artifacts\db\uploadcsv.db"
    if os.path.exists(uploaded_db_path):
        os.remove(uploaded_db_path)
        st.sidebar.success("Uploaded DB cleared.")
    else:
        st.sidebar.warning("No uploaded DB found")



data_prep_conntection = DatabasePreparationAndConnection()
stored_engine = data_prep_conntection.create_sqldb_from_csv()
data_prep_conntection.sql_connection_check()
data_prep_conntection.csv_connection_check(engine=stored_engine)

# Audio Query Code

if query_option=="Audio":
    audio_file = st.audio_input("Record your query")

    if audio_file is not None:
        # Define the save path for the recorded audio
        audio_save_path = os.path.join(os.getcwd(),'artifacts','audio_data', "recorded_query.wav")

        # Save the recorded audio file locally
        with open(audio_save_path, "wb") as f:
            f.write(audio_file.getbuffer())  # Writes the audio file buffer to the specified path


        audio_query = AudioQuery()
        model_transcript = audio_query.transcribe_audio(audio_path=audio_save_path)
        final_transcript = audio_query.get_llm_filteration(actual_transcript=model_transcript)

        # st.write("Model Transcript: ",model_transcript)
        st.write("Query: ",final_transcript)

        user_input = final_transcript

        submit_btn = st.button("🚀 Submit")

        if submit_btn:

            try:
                if chat_type == "Chat with stored SQL-DB":
                    sql_agent_from_sql_data = SQLAgentWithSQLData()
                    output = sql_agent_from_sql_data.create_sql_agent_from_sql_data(question=user_input)
                    print(output)

                elif chat_type == "Chat with stored CSV-DB":
                    sql_agent_with_csv_data = SQLAgentWithCSVData()
                    output = sql_agent_with_csv_data.create_sql_agent_from_csv_data(engine=stored_engine,question=user_input)
                    print(output)

                elif chat_type == "Chat with Uploaded CSV-DB":
                    if uploaded_engine is None:
                        uploaded_db_path = os.path.join(os.getcwd(),"artifacts","db","uploadcsv.db")
                        if os.path.exists(uploaded_db_path):
                            os.remove(uploaded_db_path)
                        st.error("Please upload a CSV/XLSX file first")
                        output = ''
                    else:
                        sql_agent_with_upload_csv_data = SQLAgentWithUploadCSVData()
                        output = sql_agent_with_upload_csv_data.create_sql_agent_from_upload_csv_data(engine=uploaded_engine,question=user_input)
                        print(output)

                if output:
                    st.text_area(
                        "🤖 Agent Response",
                        value=output,
                        height=320,
                        key="assistant_output_box",
                        disabled=True  # Makes it read-only
                    )
                else:
                    st.warning("No response generated")

            except Exception as e:
                raise CustomException(e,sys)
        

# Text Query Code

if query_option=="Text":

    user_input = st.text_area(
        "💬 Enter your question here:",
        height=70,
        placeholder="E.g. How many records are there in the table?",
        key="chat_input_box"
    )

    submit_btn = st.button("🚀 Submit")

    if submit_btn and user_input.strip():
        try:
            if chat_type == "Chat with stored SQL-DB":
                sql_agent_from_sql_data = SQLAgentWithSQLData()
                output = sql_agent_from_sql_data.create_sql_agent_from_sql_data(question=user_input)
                print(output)

            elif chat_type == "Chat with stored CSV-DB":
                sql_agent_with_csv_data = SQLAgentWithCSVData()
                output = sql_agent_with_csv_data.create_sql_agent_from_csv_data(engine=stored_engine,question=user_input)
                print(output)

            elif chat_type == "Chat with Uploaded CSV-DB":
                if uploaded_engine is None:
                    uploaded_db_path = os.path.join(os.getcwd(),"artifacts","db","uploadcsv.db")
                    if os.path.exists(uploaded_db_path):
                        os.remove(uploaded_db_path)
                    st.error("Please upload a CSV/XLSX file first")
                    output = ''
                else:
                    sql_agent_with_upload_csv_data = SQLAgentWithUploadCSVData()
                    output = sql_agent_with_upload_csv_data.create_sql_agent_from_upload_csv_data(engine=uploaded_engine,question=user_input)
                    print(output)

            if output:
                st.text_area(
                    "🤖 Agent Response",
                    value=output,
                    height=320,
                    key="assistant_output_box",
                    disabled=True  # Makes it read-only
                )
            else:
                st.warning("No response generated")

        except Exception as e:
            raise CustomException(e,sys)




