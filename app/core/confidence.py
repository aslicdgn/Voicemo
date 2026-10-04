from app.config.settings import EMOTION_CONFIDENCE_THRESHOLD

def normalize_confidence(confidence: float) -> float:
    """
    Normalize the confidence score to be between 0 and 1.
    If the confidence is greater than 1, it will be capped at 1.
    If the confidence is less than 0, it will be raised to 0.
    """
    return max(0.0, min(1.0, confidence))

def is_confident(confidence: float) -> bool:
    return normalize_confidence(confidence) >= EMOTION_CONFIDENCE_THRESHOLD