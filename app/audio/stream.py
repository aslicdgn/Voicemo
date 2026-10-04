import numpy as np
import sounddevice as sd

from app.audio.buffer import AudioBuffer
from app.audio.preprocessor import AudioPreprocessor
from app.config.settings import (
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    AUDIO_CHUNK_SECONDS
)

class AudioStream:
    def __init__(self, sample_rate=AUDIO_SAMPLE_RATE, channels=AUDIO_CHANNELS, chunk_seconds=AUDIO_CHUNK_SECONDS):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_seconds = chunk_seconds
        self.buffer = AudioBuffer(sample_rate=self.sample_rate, chunk_seconds=self.chunk_seconds)
        self.preprocessor = AudioPreprocessor()
        self.stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        audio = indata.copy()
        self.buffer.add(audio)

    def start(self):
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            callback=self._callback
        )
        self.stream.start()
    
    def stop(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def get_chunk(self) -> np.ndarray | None:
        chunk = self.buffer.get_chunk()
        if chunk is not None:
            return self.preprocessor.preprocess(chunk)
        return None