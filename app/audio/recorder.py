import sounddevice as sd
import numpy as np

from app.config.settings import AUDIO_SAMPLE_RATE, AUDIO_CHANNELS

class AudioRecorder:
    def __init__(self, sample_rate=AUDIO_SAMPLE_RATE, channels=AUDIO_CHANNELS):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = None

    def record(self, duration: float):
        frames = int(duration * self.sample_rate)
        
        audio = sd.rec(
            frames,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32"
        )
        
        sd.wait()  # Wait until recording is finished
        return audio