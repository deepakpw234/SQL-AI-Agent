from src.exception import CustomException
from src.logger import logging

from langchain_openai import ChatOpenAI
from langchain.agents import create_sql_agent