from src.exception import CustomException
from src.logger import logging
import os
import sys

from langchain.utilities import SQLDatabase

def create_sqlfile_to_sqldb(db_path):
    try:
        
        db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

    except Exception as e:
        raise CustomException(e,sys)
    
    return db