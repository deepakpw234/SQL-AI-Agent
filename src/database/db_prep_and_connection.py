from src.exception import CustomException
from src.logger import logging
import os
import sys
from dataclasses import dataclass
import pandas as pd
from sqlalchemy import create_engine, inspect
from langchain_community.utilities import SQLDatabase


@dataclass
class DatabasePreparationAndConnectionConfig:
    sql_file_dir= os.path.join(os.getcwd(),"artifacts","sql_data")
    csv_file_dir = os.path.join(os.getcwd(),"artifacts","csv_data")
    save_db_dir = os.path.join(os.getcwd(),"artifacts","db")

    sql_db_path = os.path.join(os.getcwd(),"artifacts","db","sqldb.db")
    csv_db_path = os.path.join(os.getcwd(),"artifacts","db","csv.db")


class DatabasePreparationAndConnection:
    def __init__(self):
        self.db_prep_and_connection_config = DatabasePreparationAndConnectionConfig()

    def create_sqldb_from_sqlite(self):
        '''This db has been already created by running the .read command in the terminal'''

    def create_sqldb_from_csv(self):
        try:
            if not os.path.exists(self.db_prep_and_connection_config.csv_db_path):
                for file in os.listdir(self.db_prep_and_connection_config.csv_file_dir):

                    db_path = os.path.join(self.db_prep_and_connection_config.save_db_dir,"csv.db")

                    engine = create_engine(f"sqlite:///{db_path}")

                    file_name, file_format = file.split(".")
                    if file_format == "csv":
                        df = pd.read_csv(os.path.join(self.db_prep_and_connection_config.csv_file_dir,file))
                    elif file_format == "xlsx":
                        df = pd.read_csv(os.path.join(self.db_prep_and_connection_config.csv_file_dir,file))
                    # print(df)
                    df.to_sql(file_name,engine,index=False)

            db_path = os.path.join(self.db_prep_and_connection_config.save_db_dir,"csv.db")
            engine = create_engine(f"sqlite:///{db_path}")


        except Exception as e:
            raise CustomException(e,sys)
        
        return engine
        
    def sql_connection_check(self):
        try:
            db = SQLDatabase.from_uri(f"sqlite:///{self.db_prep_and_connection_config.sql_db_path}")

            print(db.dialect)
            print(db.get_usable_table_names())
            print(db.run("select count(*) from employee"))


        except Exception as e:
            raise CustomException(e,sys)
        
    def csv_connection_check(self,engine):
        try:

            db = SQLDatabase(engine=engine)
            print(db.dialect)
            print(db.get_usable_table_names())
            print(db.run("select count(*) from cancer"))


        except Exception as e:
            raise CustomException(e,sys)
        

if __name__=="__main__":
    data_prep_conntection = DatabasePreparationAndConnection()
    engine = data_prep_conntection.create_sqldb_from_csv()
    data_prep_conntection.sql_connection_check()
    data_prep_conntection.csv_connection_check(engine=engine)