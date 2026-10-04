"""The Voicemo application window.

    [ Open audio file ] ....................... [ Analyze ]
    ┌───────────────────┐  ┌──────────────────────────────┐
    │   emotion (hero)  │  │           transcript         │
    └───────────────────┘  └──────────────────────────────┘
    status line

Every analysis runs on a background AnalysisWorker and is tagged with a run id.
Starting an analysis clears the display first and bumps the id, so the panels
can never keep showing a previous file's result, and a stale result arriving
late is ignored. The status line names the file being analysed, which makes it
obvious at a glance which audio produced the result on screen.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.ui.components import EmotionCard, TranscriptPanel
from app.ui.emotion_style import DisplayResult
from app.ui.theme import load_stylesheet
from app.ui.worker import AnalysisWorker

_AUDIO_FILTER = "Audio files (*.wav *.mp3 *.m4a *.flac *.ogg);;All files (*)"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Voicemo")
        self.resize(900, 600)
        self.setMinimumSize(780, 520)

        self._audio_path: Path | None = None
        self._run_id = 0
        self._workers: list[AnalysisWorker] = []

        self._build_ui()
        self.setStyleSheet(load_stylesheet())

    # ------------------------------------------------------------------ build
    def _build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("root")

        outer = QVBoxLayout(root)
        outer.setContentsMargins(28, 24, 28, 22)
        outer.setSpacing(20)

        outer.addLayout(self._build_header())
        outer.addLayout(self._build_controls())
        outer.addLayout(self._build_body(), stretch=1)

        self._status = QLabel("Ready")
        self._status.setObjectName("status")
        outer.addWidget(self._status)

        self.setCentralWidget(root)

    def _build_header(self) -> QVBoxLayout:
        title = QLabel("Voicemo")
        title.setObjectName("appTitle")
        subtitle = QLabel("Speech emotion analysis for accessible online meetings")
        subtitle.setObjectName("appSubtitle")
        box = QVBoxLayout()
        box.setSpacing(3)
        box.addWidget(title)
        box.addWidget(subtitle)
        return box

    def _build_controls(self) -> QHBoxLayout:
        self._open_btn = QPushButton("Open audio file")
        self._open_btn.clicked.connect(self._on_open_file)

        self._file_label = QLabel("No audio selected")
        self._file_label.setObjectName("fileName")

        self._analyze_btn = QPushButton("Analyze")
        self._analyze_btn.setObjectName("primary")
        self._analyze_btn.setEnabled(False)
        self._analyze_btn.clicked.connect(self._on_analyze)

        row = QHBoxLayout()
        row.setSpacing(12)
        row.addWidget(self._open_btn)
        row.addSpacing(6)
        row.addWidget(self._file_label, stretch=1)
        row.addWidget(self._analyze_btn)
        return row

    def _build_body(self) -> QGridLayout:
        self._emotion_card = EmotionCard()
        self._transcript = TranscriptPanel()
        body = QGridLayout()
        body.setSpacing(20)
        body.addWidget(self._emotion_card, 0, 0)
        body.addWidget(self._transcript, 0, 1)
        body.setColumnStretch(0, 4)
        body.setColumnStretch(1, 6)
        return body

    # --------------------------------------------------------------- file I/O
    def _on_open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select audio file", "", _AUDIO_FILTER
        )
        if path:
            self._set_audio(Path(path))

    def _set_audio(self, path: Path) -> None:
        self._audio_path = path
        self._file_label.setText(path.name)
        self._analyze_btn.setEnabled(True)
        self._status.setText(f"Loaded {path.name}")

    # --------------------------------------------------------------- analysis
    def _on_analyze(self) -> None:
        if self._audio_path is None:
            return

        self._run_id += 1
        run_id = self._run_id
        name = self._audio_path.name

        # clear the previous result up front so nothing stale can linger
        self._emotion_card.show_waiting()
        self._transcript.clear()
        self._set_busy(True)
        self._status.setText(f"Analyzing {name}")

        worker = AnalysisWorker(run_id, self._audio_path)
        worker.succeeded.connect(self._on_result)
        worker.failed.connect(self._on_error)
        worker.finished.connect(lambda w=worker: self._cleanup_worker(w))
        self._workers.append(worker)  # keep a reference so it isn't GC'd
        worker.start()

    def _on_result(self, run_id: int, result: DisplayResult) -> None:
        if run_id != self._run_id:
            return  # a newer analysis has superseded this one
        self._emotion_card.show_result(result)
        self._transcript.set_text(result.transcript)
        self._status.setText(f"Done — {result.label.lower()}")
        self._set_busy(False)

    def _on_error(self, run_id: int, message: str) -> None:
        if run_id != self._run_id:
            return
        self._emotion_card.reset()
        self._status.setText(f"Couldn't analyze: {message}")
        self._set_busy(False)
        QMessageBox.warning(self, "Analysis failed", message)

    def _cleanup_worker(self, worker: AnalysisWorker) -> None:
        if worker in self._workers:
            self._workers.remove(worker)
        worker.deleteLater()

    def _set_busy(self, busy: bool) -> None:
        self._open_btn.setEnabled(not busy)
        self._analyze_btn.setEnabled(not busy and self._audio_path is not None)