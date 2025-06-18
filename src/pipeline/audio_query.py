import whisper
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU*")
from dataclasses import dataclass
import os
import sys

from src.exception import CustomException
from src.logger import logging


import openai
from dotenv import load_dotenv
load_dotenv()

@dataclass
class AudioQueryConfig:
    audio_dir_path = os.path.join(os.getcwd(),'artifacts','audio_data')
    audio_file_path = os.path.join(os.getcwd(),'artifacts','audio_data','recorded_query.wav')

class AudioQuery:
    def __init__(self):
        self.audio_query_config = AudioQueryConfig()

    
    def transcribe_audio(self , audio_path):
        try:
            # model = whisper.load_model("base")
            # result = model.transcribe(audio_path)

            audio_file = open(audio_path,'rb')

            response = openai.audio.transcriptions.create(
                model='gpt-4o-mini-transcribe',
                file=audio_file,
                response_format='text'
            )
            
        except Exception as e:
            raise CustomException(e,sys)

        return response
    
    
    def get_llm_filteration(self,actual_transcript):
        try:
            llm = ChatOpenAI()

            template = PromptTemplate.from_template(
                "You are a helpful assistant that convert the following transcript into well-structured and grammatically correct English, ensuring there are no spelling errors. Transcript:\n{transcript}"
            )

            chain = template | llm

            final_transcript = chain.invoke({'transcript':actual_transcript})

        except Exception as e:
            raise CustomException(e,sys)
        
        return final_transcript.content
    

# if __name__=="__main__":
#     file_path = r"C:\Users\deepa\Panda 2024\GenAI\SQL Agent\artifacts\audio_data\recorded_query.wav"
#     a = AudioQuery()
#     b = a.transcribe_audio(file_path)
#     c = a.get_llm_filteration(b)
#     print("b : ",b)
#     print("c : ",c)








