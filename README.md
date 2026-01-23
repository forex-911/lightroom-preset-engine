# Cinematic Lightroom Preset Generator

A GenAI-powered system that generates **cinematic Adobe Lightroom presets** by analyzing image differences. Separates **semantic intent (AI)** from **deterministic parameter generation** to avoid hallucination.

## Features

- Image difference analysis
- AI-powered semantic style inference
- Deterministic Lightroom parameter generation
- Lightroom `.xmp` preset export
- FastAPI backend

## Project Structure
```
.
├── backend/
│   ├── main.py
│   ├── ai_layer.py
│   ├── image_analysis.py
│   └── preset_engine.py
├── presets/
│   └── generated/
├── .env
├── requirements.txt
└── README.md
```

## Installation
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
python -m venv venv
source venv/bin/activate  # Linux/Mac or venv\Scripts\activate for Windows
pip install -r requirements.txt
```

## Configuration

Create `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

Create `.gitignore`:
```
.env
venv/
__pycache__/
*.pyc
presets/generated/*.xmp
```

## Usage
```bash
uvicorn backend.main:app --reload
```

- Server: `http://127.0.0.1:8000`
- API Docs: `http://127.0.0.1:8000/docs`

## API Endpoints

**POST** `/generate-preset`
- Upload reference and target images
- Returns `.xmp` preset file

**GET** `/download/{filename}`
- Download generated preset

## License

MIT License
