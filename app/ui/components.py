"""Reusable widgets that make up the main window's body.

Two panels: the emotion display (the hero — a large emoji, the emotion word and
a confidence bar, recoloured to the detected emotion) and the transcript panel.
Both expose small, explicit methods the window calls as analysis progresses, so
the window never reaches inside them to poke individual labels.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QProgressBar,
    QTextEdit,
    QVBoxLayout,
)

from app.ui.emotion_style import DisplayResult


class Card(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("card")


class EmotionCard(Card):
    """The hero: large emoji, emotion word, and a confidence bar."""

    def __init__(self) -> None:
        super().__init__()

        self._emoji = QLabel("\U0001F3A4")  # 🎤
        self._emoji.setObjectName("emotionEmoji")
        self._emoji.setAlignment(Qt.AlignCenter)

        self._label = QLabel("Ready")
        self._label.setObjectName("emotionLabel")
        self._label.setAlignment(Qt.AlignCenter)

        self._bar = QProgressBar()
        self._bar.setRange(0, 100)
        self._bar.setValue(0)
        self._bar.setTextVisible(False)

        self._meta = QLabel("Load or record audio to begin")
        self._meta.setObjectName("emotionMeta")
        self._meta.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 32, 28, 28)
        layout.setSpacing(16)
        layout.addStretch(1)
        layout.addWidget(self._emoji)
        layout.addWidget(self._label)
        layout.addWidget(self._bar)
        layout.addWidget(self._meta)
        layout.addStretch(1)

    def show_result(self, result: DisplayResult) -> None:
        self._emoji.setText(result.emoji)
        self._label.setText(result.label)
        self._label.setStyleSheet(f"color: {result.color};")
        self._bar.setRange(0, 100)
        self._bar.setValue(round(result.confidence * 100))
        self._bar.setStyleSheet(
            "QProgressBar::chunk { border-radius: 5px; "
            f"background-color: {result.color}; }}"
        )
        pct = f"{result.confidence * 100:.0f}%"
        self._meta.setText(
            f"{pct} confidence" if result.confident else f"Low confidence ({pct})"
        )

    def show_waiting(self) -> None:
        self._emoji.setText("\u23F3")  # ⏳
        self._label.setText("Analyzing")
        self._label.setStyleSheet("")
        self._bar.setStyleSheet("")
        self._bar.setRange(0, 0)  # indeterminate (busy) animation
        self._meta.setText("Running Whisper and emotion2vec")

    def reset(self) -> None:
        self._emoji.setText("\U0001F3A4")
        self._label.setText("Ready")
        self._label.setStyleSheet("")
        self._bar.setStyleSheet("")
        self._bar.setRange(0, 100)
        self._bar.setValue(0)
        self._meta.setText("Load or record audio to begin")


class TranscriptPanel(Card):
    """Shows the recognised speech."""

    def __init__(self) -> None:
        super().__init__()

        heading = QLabel("Transcript")
        heading.setObjectName("panelHeading")

        self._text = QTextEdit()
        self._text.setObjectName("transcript")
        self._text.setReadOnly(True)
        self._text.setPlaceholderText("The transcript will appear here.")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 20)
        layout.setSpacing(12)
        layout.addWidget(heading)
        layout.addWidget(self._text, stretch=1)

    def set_text(self, text: str) -> None:
        self._text.setPlainText(text or "(No speech detected.)")

    def clear(self) -> None:
        self._text.clear()