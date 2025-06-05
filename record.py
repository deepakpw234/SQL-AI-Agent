import streamlit as st
import json
from streamlit_webrtc import webrtc_streamer  # WebRTC for live recording
import whisper
import tempfile
import os
import torch

import whisper
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU*")
import sys
import asyncio
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) 


st.title("🎙️ Audio Recorder")


# Ensure directory for storing audio responses
AUDIO_SAVE_PATH = os.path.join(os.getcwd(),'artifacts','audio_data')
os.makedirs(AUDIO_SAVE_PATH, exist_ok=True)  # Creates the directory if it doesn't exist


# Audio Recording Section
audio_file = st.audio_input("Record your query")  # Allows users to record audio input

if audio_file is not None:
    # Define the save path for the recorded audio
    audio_save_path = os.path.join(AUDIO_SAVE_PATH, "recorded_query.wav")

    # Save the recorded audio file locally
    with open(audio_save_path, "wb") as f:
        f.write(audio_file.getbuffer())  # Writes the audio file buffer to the specified path

    st.write(f"Audio saved at: {audio_save_path}")  # Display the save path for reference
    st.audio(audio_file)  # Playback the recorded audio

    # Load model
    model = whisper.load_model("base")

    # Transcribe audio
    def transcribe_audio(audio_path):
        result = model.transcribe(audio_path)
        return result["text"]


    # Initialize the LLM
    llm = ChatOpenAI(temperature=0.2)

    # Define a processing template
    template = PromptTemplate.from_template(
        "You are a helpful assistant that convert the following transcript into well-structured and grammatically correct English, ensuring there are no spelling errors. Transcript:\n{transcript}"
    )

    # Create chain
    intent_chain = template | llm

    # Use transcription

    audio_path = r"C:\Users\deepa\Panda 2024\GenAI\SQL Agent\artifacts\audio_data\recorded_query.wav"

    transcript = transcribe_audio(audio_path)
    transcript_without_grammer_mistakes = intent_chain.invoke(transcript)

    print("transcript: ",transcript)
    print("User Intent:", transcript_without_grammer_mistakes.content)

    st.write(transcript)
    st.write(transcript_without_grammer_mistakes.content)


    