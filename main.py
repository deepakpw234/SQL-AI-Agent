from src.exception import CustomException
from src.logger import logging
import os
import sys

from src.database.db_prep_and_connection import DatabasePreparationAndConnection
from src.agents.agent_with_sql import SQLAgentWithSQLData
from src.agents.agent_with_csv import SQLAgentWithCSVData

if __name__=="__main__":
    try:
        data_prep_conntection = DatabasePreparationAndConnection()
        engine = data_prep_conntection.create_sqldb_from_csv()
        data_prep_conntection.sql_connection_check()
        data_prep_conntection.csv_connection_check(engine=engine)

        # question = 'how many albums are there?'
        # database = "sql"

        question = 'how many patients are there in the cancer table'
        database = "csv"

        if database=="sql":

            sql_agent_from_sql_data = SQLAgentWithSQLData()
            output = sql_agent_from_sql_data.create_sql_agent_from_sql_data(question=question)
            print(output)

        elif database=="csv":

            sql_agent_with_csv_data = SQLAgentWithCSVData()
            output = sql_agent_with_csv_data.create_sql_agent_from_csv_data(engine=engine,question=question)
            print(output)

    except Exception as e:
        raise CustomException(e,sys)

