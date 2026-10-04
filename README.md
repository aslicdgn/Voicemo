# Voicemo

An accessibility-focused desktop application that analyzes speech emotion during online meetings and represents estimated emotional tone using emojis.

## Planned Features

* Turkish and English speech recognition
* Speech emotion recognition
* Whisper integration
* emotion2vec integration
* PyTorch-based inference
* Real-time emotion visualization
* Emoji-based emotional cues
* Local-first processing
* Accessibility-focused meeting experience

## Tech Stack

* Python 3.12
* PySide6
* PyTorch
* Whisper
* emotion2vec
* ONNX Runtime
* pytest

## Development

### 1. Clone the repository

```bash
git clone <repository-url>
cd Voicemo
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

This installs the required application dependencies, including PySide6, as well as development tools such as pytest and pytest-qt.

### 5. Start the UI

Run the application with:

```bash
python -m app.main
```

### 6. Run tests

```bash
python -m pytest
```

## Project Structure

```text
Voicemo/
├── app/
│   ├── audio/
│   ├── config/
│   ├── core/
│   ├── inference/
│   ├── models/
│   ├── ui/
│   ├── utils/
│   └── main.py
├── models/
│   ├── whisper/
│   └── emotion2vec/
├── tests/
├── docs/
├── .github/
│   └── workflows/
├── .gitignore
├── README.md
└── pyproject.toml
```

## Model Pipeline

```text
Audio Input
     │
     ├───────────────┐
     ↓               ↓
  Whisper        emotion2vec
     │               │
     ↓               ↓
Transcript     Emotional Tone
     │               │
     └───────┬───────┘
             ↓
      Emotion Engine
             ↓
       Emoji / UI
```

## License

This project is currently under development.
