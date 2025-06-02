from src.exception import CustomException
from src.logger import logging
import os
import sys
from dataclasses import dataclass
import pandas as pd
from sqlalchemy import create_engine, inspect
from langchain_community.utilities import SQLDatabase


@dataclass
class UploadedFileDatabasePreparationConfig:
    sql_file_dir= os.path.join(os.getcwd(),"artifacts","sql_data")
    upload_csv_file_dir = os.path.join(os.getcwd(),"artifacts","upload_data")
    save_db_dir = os.path.join(os.getcwd(),"artifacts","db")

    sql_db_path = os.path.join(os.getcwd(),"artifacts","db","sqldb.db")
    csv_db_path = os.path.join(os.getcwd(),"artifacts","db","uploadcsv.db")


class UploadedFileDatabasePreparation:
    def __init__(self):
        self.upload_file_db_prep_config = UploadedFileDatabasePreparationConfig()

    def create_sqldb_from_csv(self):
        try:
            if not os.path.exists(self.upload_file_db_prep_config.csv_db_path):
                for file in os.listdir(self.upload_file_db_prep_config.upload_csv_file_dir):

                    db_path = os.path.join(self.upload_file_db_prep_config.save_db_dir,"uploadcsv.db")

                    engine = create_engine(f"sqlite:///{db_path}")

                    file_name, file_format = file.split(".")
                    if file_format == "csv":
                        df = pd.read_csv(os.path.join(self.upload_file_db_prep_config.upload_csv_file_dir,file))
                    elif file_format == "xlsx":
                        df = pd.read_csv(os.path.join(self.upload_file_db_prep_config.upload_csv_file_dir,file))
                    # print(df)
                    df.to_sql(file_name,engine,index=False)

            db_path = os.path.join(self.upload_file_db_prep_config.save_db_dir,"uploadcsv.db")
            engine = create_engine(f"sqlite:///{db_path}")


        except Exception as e:
            raise CustomException(e,sys)
        
        return engine
        
    def csv_connection_check(self,engine):
        try:

            db = SQLDatabase(engine=engine)
            # print(db.dialect)
            # print(db.get_usable_table_names())
            # print(db.run('select * from vidhan WHERE "PC NAME"="Aruku"; '))
            # print(db.run('PRAGMA table_info(vidhan);'))
            # # print(db.run('PRAGMA table_info(cancer);'))


        except Exception as e:
            raise CustomException(e,sys)
        
