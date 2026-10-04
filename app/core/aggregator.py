from collections import Counter

class EmotionAggregator:
    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.history = []

    def add_emotion(self, emotion: str, confidence: float):
        self.history.append({
            "emotion": emotion,
            "confidence": confidence
        })
        
        if len(self.history) > self.window_size:
            self.history.pop(0)
        
        scores = {}

        for item in self.history:
            emotion = item["emotion"]
            confidence = item["confidence"]
            scores[emotion] = scores.get(emotion, 0.0) + confidence

        return max(scores, key=scores.get)