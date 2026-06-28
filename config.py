import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

# MODEL_NAME = "gemini-2.5-flash"
MODEL_NAME = "gemini-3.1-flash-lite"

SAMPLE_RATE = 16000
CHANNELS = 1
RECORDING_PATH = "recordings/input.wav"

RESPONSE_AUDIO_PATH = (
    "recordings/response.mp3"
)