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
class SQLAgentWithCSVDataConfig:
    csv_db_path = os.path.join(os.getcwd(),"artifacts","db","csv.db")


class SQLAgentWithCSVData:
    def __init__(self):
        self.sql_agent_csv_config = SQLAgentWithCSVDataConfig()


    def create_sql_agent_from_csv_data(self,engine):
        try:
            llm = ChatOpenAI()

            db = SQLDatabase(engine=engine)

            csv_agent_executor = create_sql_agent(llm=llm,db=db,agent_type='openai-tools')

            question = 'how many patients are there in the cancer table'

            csv_query_result = csv_agent_executor.invoke({'input':question})

            print(csv_query_result['output'])

        except Exception as e:
            raise CustomException(e,sys)
        

if __name__=="__main__":
    sql_agent_with_csv = SQLAgentWithCSVData()
    a = DatabasePreparationAndConnection()
    res = a.create_sqldb_from_csv()
    sql_agent_with_csv.create_sql_agent_from_csv_data(res)
