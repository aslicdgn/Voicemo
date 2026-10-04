from pathlib import Path

import whisper


class WhisperModel:
    """Wrapper around the OpenAI Whisper speech recognition model."""

    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path: str | Path) -> str:
        result = self.model.transcribe(
            str(audio_path),
            language=None,
        )

        return result["text"].strip()