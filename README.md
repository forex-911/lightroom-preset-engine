# Cinematic Lightroom Preset Generator

A GenAI-powered system that generates **cinematic Adobe Lightroom presets** by analyzing image differences. Separates **semantic intent (AI)** from **deterministic parameter generation** to avoid hallucination.

## Features

- Image difference analysis
- AI-powered semantic style inference
- Deterministic Lightroom parameter generation
- Lightroom `.xmp` preset export
- FastAPI backend + Simple frontend

## Project Structure
```
.
├── backend/
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   ├── color_safety.py
│   │   ├── feature_diff.py
│   │   ├── image_analysis.py
│   │   ├── lab_color_transfer.py
│   │   ├── llm_service.py
│   │   └── preset_generator.py
│   ├── .env
│   ├── config.py
│   └── main.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── .env.example
├── README.md
└── requirements.txt
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

Create `.env` file in the `backend/` directory:
```
GEMINI_API_KEY=your_api_key_here
```

Create `.gitignore`:
```
.env
backend/.env
venv/
__pycache__/
*.pyc
*.xmp
```

## Usage

### Start Backend Server
```bash
cd backend
uvicorn main:app --reload
```

- Backend API: `http://127.0.0.1:8000`
- API Docs: `http://127.0.0.1:8000/docs`

### Open Frontend

Open `frontend/index.html` in your browser or serve it with:
```bash
cd frontend
python -m http.server 8080
```

Then visit `http://localhost:8080`

## API Endpoints

**POST** `/generate-preset`
- Upload reference and target images
- Returns `.xmp` preset file

**GET** `/download/{filename}`
- Download generated preset

## License

MIT License
