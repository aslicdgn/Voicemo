from app.models.whisper_model import WhisperModel
from app.models.emotion2vec_model import Emotion2VecModel
from app.core.emotion_engine import EmotionEngine

class VoicemoPipeline:
    def __init__(self):
        self.whisper_model = WhisperModel()
        self.emotion2vec_model = Emotion2VecModel()
        self.emotion_engine = EmotionEngine()

    def process(self, audio_file_path: str):
        # Step 1: Transcribe the audio using Whisper
        transcription = self.whisper_model.transcribe(audio_file_path)

        # Step 2: Analyze the emotion from the transcribed text using Emotion2Vec
        emotion_result = self.emotion2vec_model.predict(audio_file_path)

        # Step 3: Process the emotion and get the corresponding emoji
        emotion = self.emotion_engine.process(
            emotion_result["emotion"],
            emotion_result["confidence"]
        )

        return {
            "transcription": transcription,
            "emotion": emotion.emotion,
            "confidence": emotion.confidence,
            "emoji": emotion.emoji
        }