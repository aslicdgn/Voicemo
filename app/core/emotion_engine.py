from dataclasses import dataclass

@dataclass
class EmotionResult:
    emotion: str
    confidence: float
    emoji: str
    

class EmotionEngine:
    def __init__(self):
        # Initialize any necessary resources or models here
        pass

    EMOTION_EMOJI_MAP = {
        "happy": "😊",
        "sad": "😢",
        "angry": "😠",
        "fearful": "😨",
        "surprised": "😮",
        "disgusted": "🤢",
        "neutral": "😐",
        "other": "❓",
        "unknown": "❓",
    }
    
    def process(self, emotion: str, confidence: float) -> EmotionResult:
        """
        Process the detected emotion and return an EmotionResult object.

        Args:
            emotion (str): The detected emotion.
            confidence (float): The confidence score of the detected emotion.

        Returns:
            EmotionResult: An object containing the processed emotion, confidence, and emoji.
        """
        emoji = self.EMOTION_EMOJI_MAP.get(emotion, "❓")
        
        if not emoji:
            emoji = "❓"
            
        return EmotionResult(emotion=emotion, confidence=confidence, emoji=emoji)