import numpy as np
import whisper


class WhisperModel:
    """Wrapper around the OpenAI Whisper speech recognition model."""

    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio: np.ndarray) -> str:
        result = self.model.transcribe(
            audio,
            language=None,
        )

        return result["text"].strip()