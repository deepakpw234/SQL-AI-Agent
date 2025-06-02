from src.exception import CustomException
from src.logger import logging
import os
import sys
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase

from dataclasses import dataclass
from src.database.db_prep_and_connection import DatabasePreparationAndConnection


@dataclass
class SQLAgentWithUploadCSVDataConfig:
    upload_csv_db_path = os.path.join(os.getcwd(),"artifacts","db","uploadcsv.db")


class SQLAgentWithUploadCSVData:
    def __init__(self):
        self.sql_agent_csv_config = SQLAgentWithUploadCSVDataConfig()


    def create_sql_agent_from_upload_csv_data(self,engine,question):
        try:
            llm = ChatOpenAI()

            db = SQLDatabase(engine=engine)

            csv_agent_executor = create_sql_agent(llm=llm,db=db,agent_type='openai-tools',verbose=True)

            csv_query_result = csv_agent_executor.invoke({'input':question})

            result = csv_query_result['output']

        except Exception as e:
            raise CustomException(e,sys)
        
        return result
        
