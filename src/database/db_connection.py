from src.exception import CustomException
from src.logger import logging
import os
import sys
from dataclasses import dataclass
import pandas as pd
from langchain_community.utilities import SQLDatabase

from src.database.db_prep import DatabasePreparation
from sqlalchemy import inspect

@dataclass
class DatabaseConnectionConfig:
    sql_db_path = os.path.join(os.getcwd(),"artifacts","sqldb.db")
    csv_db_path = os.path.join(os.getcwd(),"artifacts","csv.db")


class DatabaseConnection:
    def __init__(self):
        self.database_connection = DatabaseConnectionConfig()

    def sql_connection(self):
        db = SQLDatabase.from_uri(f"sqlite:///{self.database_connection.sql_db_path}")

        print(db.dialect)
        print(db.get_usable_table_names())
        print(db.run("select count(*) from employee"))

    def csv_connection(self,engine):
        # db = SQLDatabase(engine)
        # print(db.dialect)
        # print(db.get_usable_table_names())
        # print(db.run("select count(*) from cancer"))
        insp = inspect(engine)
        table_name = insp.get_table_names()
        print(table_name)


if __name__=="__main__":
    data_connection = DatabaseConnection()
    data_connection.sql_connection()

    req = DatabasePreparation().create_sql_database_from_csv()

    data_connection.csv_connection(req)