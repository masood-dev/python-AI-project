# StudyChat AI

A chat-based study assistant powered by AI. Upload documents and ask questions about them.

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Run with Ollama (local):
```bash
# Make sure Ollama is running on localhost:11434
uvicorn app.main:app --reload
```

Run with Hugging Face (cloud):
```bash
# Set HUGGINGFACE_API_KEY in .env
AI_PROVIDER=huggingface uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173

## API Documentation

Once backend is running, visit http://localhost:8000/docs for interactive API docs.

## Simplified for Text-Only Chat

- No flashcards or interactive widgets
- Pure text-based conversation like ChatGPT
- Upload documents (PDF, DOCX, TXT) for context
- Simple, clean interface

## Architecture

- **Backend**: FastAPI + MongoDB + Motor (async)
- **Frontend**: React 18 + Vite
- **AI**: Ollama (dev) or Hugging Face (prod)
- **Deployment**: AWS Lambda + S3 + CloudFront

## Free Tier Constraints

- MongoDB Atlas M0 (512MB)
- AWS Lambda Free Tier (1M requests/month)
- Hugging Face free Serverless Inference API
- No OpenAI or paid APIs

See `PROJECT_BRIEF.md` for detailed specifications.
