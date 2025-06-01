from src.exception import CustomException
from src.logger import logging
import os
import sys
from dataclasses import dataclass
import pandas as pd
from sqlalchemy import create_engine, inspect
from langchain_community.utilities import SQLDatabase

@dataclass
class DatabasePreparationConfig:
    sql_file_dir= os.path.join(os.getcwd(),"artifacts","sql_data")
    sql_db_dir = os.path.join(os.getcwd(),"artifacts")
    csv_file_dir = os.path.join(os.getcwd(),"artifacts","csv_data")


class DatabasePreparation:
    def __init__(self):
        self.database_preparation_config = DatabasePreparationConfig()


    def create_sql_database_from_sqlfile(self,db_path):
        pass


    def create_sql_database_from_csv(self):
        try:
            for file in os.listdir(data_config.database_preparation_config.csv_file_dir):

                db_path = os.path.join(data_config.database_preparation_config.sql_db_dir,"csv.db")

                print(db_path)
                engine = create_engine(f"sqlite:///{db_path}")

                file_name, file_format = file.split(".")
                if file_format == "csv":
                    df = pd.read_csv(os.path.join(data_config.database_preparation_config.csv_file_dir,file))
                elif file_format == "xlsx":
                    df = pd.read_csv(os.path.join(data_config.database_preparation_config.csv_file_dir,file))
                # print(df)
                df.to_sql(file_name,engine,index=False)

            # db = SQLDatabase(engine=engine)
            # print(db.dialect)
            # print(db.get_usable_table_names())
            # print(db.run("select * from cancer"))

            # insp = inspect(engine)
            # table = insp.get_table_names()
            # print(table)

        except Exception as e:
            raise CustomException(e,sys)
        
        return engine


if __name__=="__main__":
    data_config = DatabasePreparation()
    data_config.create_sql_database_from_csv()
