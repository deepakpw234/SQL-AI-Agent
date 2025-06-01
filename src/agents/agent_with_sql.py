from src.exception import CustomException
from src.logger import logging
import os
import sys

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents import AgentExecutor
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
load_dotenv()

from dataclasses import dataclass

@dataclass
class SQLAgentWithSQLDataConfig:
    sql_db_path = os.path.join(os.getcwd(),"artifacts","db","sqldb.db")


class SQLAgentWithSQLData:
    def __init__(self):
        self.sql_agent_config = SQLAgentWithSQLDataConfig()

    def create_sql_agent_from_sql_data(self):
        try:
            llm = ChatOpenAI()

            db = SQLDatabase.from_uri(f"sqlite:///{self.sql_agent_config.sql_db_path}")

            sql_agent_executor = create_sql_agent(llm=llm,db=db,agent_type='openai-tools')

            question = 'how many albums are there?'

            query_result = sql_agent_executor.invoke({'input':question})

            print(query_result['output'])


        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    sql_agent_from_sql_data = SQLAgentWithSQLData()
    sql_agent_from_sql_data.create_sql_agent_from_sql_data()
    