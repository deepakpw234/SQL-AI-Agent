import whisper
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU*")


# Load model
model = whisper.load_model("base")  # Or "small", "medium", "large"

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

audio_path = r"C:\Users\deepa\Panda 2024\GenAI\SQL Agent\artifacts\audio_data\Recording.mp3"

transcript = transcribe_audio(audio_path)
intent = intent_chain.invoke(transcript)

print("transcript: ",transcript)
print("User Intent:", intent.content)




