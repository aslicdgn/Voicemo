from collections import deque
from app.config.settings import AUDIO_CHUNK_SECONDS
import numpy as np

class AudioBuffer:
    def __init__(self, sample_rate: int = 16000, chunk_seconds: float = AUDIO_CHUNK_SECONDS):
        self.sample_rate = sample_rate
        self.chunk_seconds = chunk_seconds
        self.chunk_size = int(self.sample_rate * self.chunk_seconds)
        self.buffer = deque()
        self.sample_count = 0

    def add(self, audio: np.ndarray) -> None:
        audio = np.asarray(audio, dtype=np.float32)
        if audio.ndim > 1:
            audio = audio.reshape(-1)  # Flatten to 1D if necessary
        self.buffer.append(audio)
        self.sample_count += len(audio)

    def is_ready(self) -> bool:
        return self.sample_count >= self.chunk_size
    
    def get_chunk(self) -> np.ndarray | None:
        if not self.is_ready():
            return None
        
        samples = []
        remaining = self.chunk_size
        while remaining > 0 and self.buffer:
            current = self.buffer.popleft()
            if len(current) <= remaining:
                samples.append(current)
                remaining -= len(current)
                self.sample_count -= len(current)
            else:
                samples.append(current[:remaining])
                leftover = current[remaining:]
                self.buffer.appendleft(leftover)
                self.sample_count -= remaining
                remaining = 0
        return np.concatenate(samples).astype(np.float32) if samples else None

    def clear(self) -> None:
        self.buffer.clear()
        self.sample_count = 0