from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
EMOTION2VEC_MODEL_DIR = MODELS_DIR / "emotion2vec"

WHISPER_MODEL_NAME = "base"  # Options: tiny, base, small, medium, large
WHISPER_LANGUAGE = None  # Set to None for automatic language detection

EMOTION2VEC_MODEL_PATH = EMOTION2VEC_MODEL_DIR

AUDIO_SAMPLE_RATE = 16000  # Sample rate for audio processing
AUDIO_CHANNELS = 1  # Number of audio channels (1 for mono, 2 for stereo)
AUDIO_CHUNK_SECONDS = 5.0  # Duration of each audio chunk in seconds"

EMOTION_CONFIDENCE_THRESHOLD = 0.60  # Confidence threshold for emotion detection

APP_NAME = "Voicemo"
APP_VERSION = "0.1.0"