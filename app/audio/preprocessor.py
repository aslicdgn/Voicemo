import numpy as np

class AudioPreprocessor:
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate

    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """Normalize the audio signal to the range [-1, 1]."""
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val
        return audio

    def to_mono(self, audio: np.ndarray) -> np.ndarray:
        """Convert stereo audio to mono by averaging the channels."""
        if audio.ndim == 2 and audio.shape[1] > 1:
            return np.mean(audio, axis=1)
        return audio

    def preprocess(self, audio: np.ndarray) -> np.ndarray:
        """Preprocess the audio by normalizing and converting to mono."""
        audio = self.to_mono(audio)
        audio = self.normalize_audio(audio)
        return audio.astype(np.float32)