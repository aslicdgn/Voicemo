"""Presentation styling for emotions — the UI's own layer.

The backend tells us *which* emotion was detected (and an emoji); how that
emotion should *look* on screen is a UI decision, so the accent colour and the
display word live here rather than in the backend's emotion engine. This keeps
a clean split: the backend owns detection, the UI owns appearance.

``DisplayResult`` is the small, render-ready object the window actually draws,
assembled from the backend's result plus this styling.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EmotionStyle:
    label: str   # Word shown to the user, e.g. "Happy"
    color: str   # Accent colour (hex), legible on a light surface


@dataclass(frozen=True)
class DisplayResult:
    """Everything the window needs to render one analysis."""

    transcript: str
    emotion: str        # raw label from the backend, e.g. "happy"
    confidence: float   # 0.0 – 1.0
    emoji: str          # taken from the backend result
    color: str
    label: str
    confident: bool = True   # False when below the backend's confidence threshold


# Colours are picked for contrast on a white card and to stay distinct from one
# another, so emotion can be read from colour as well as from the word/emoji.
_STYLES: dict[str, EmotionStyle] = {
    "angry":     EmotionStyle("Angry",     "#D64545"),
    "disgusted": EmotionStyle("Disgusted", "#5E8C3E"),
    "fearful":   EmotionStyle("Fearful",   "#6B5BD2"),
    "happy":     EmotionStyle("Happy",     "#C98A00"),
    "neutral":   EmotionStyle("Neutral",   "#6B7280"),
    "sad":       EmotionStyle("Sad",       "#3B74C4"),
    "surprised": EmotionStyle("Surprised", "#C14D9E"),
    "other":     EmotionStyle("Other",     "#6B7280"),
    "unknown":   EmotionStyle("Unknown",   "#9AA2AE"),
}

_FALLBACK = EmotionStyle("Unknown", "#9AA2AE")


def style_for(emotion: str) -> EmotionStyle:
    return _STYLES.get((emotion or "").lower(), _FALLBACK)