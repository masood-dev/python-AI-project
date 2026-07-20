# StudyChat AI

A portfolio project: text-based AI chat application for studying with PDF/DOCX document uploads and AI-powered responses.

## Features

- 💬 **Text-based Chat** - Clean, Claude-like UI dark theme
- 📄 **Document Upload** - Support for PDF, DOCX, TXT files
- 🤖 **AI Responses** - Powered by Ollama (local) or Hugging Face (cloud)
- 💾 **Session Management** - Save and retrieve chat history
- 🔄 **Async Architecture** - FastAPI + Motor async MongoDB driver

## Tech Stack

**Frontend:**
- React 18 + Vite
- Plain CSS (dark theme, Claude-inspired design)
- Custom React hooks

**Backend:**
- Python 3.13 + FastAPI
- Motor (async MongoDB driver)
- Pydantic v2 for validation

**Database:**
- MongoDB Atlas (M0 free tier)

**AI Providers:**
- Ollama (local, development)
- Hugging Face Inference API (production)

**Deployment:**
- AWS Lambda + S3 + CloudFront (ready)

## Setup

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

Create `.env`:
```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/studychat
OPENAI_API_KEY=your_key_here
OLLAMA_BASE_URL=http://localhost:11434
```

Run:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:5173`

## Project Structure

```
python-AI-project/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app factory
│   │   ├── core/config.py       # Settings
│   │   ├── db/mongodb.py        # Async MongoDB connection
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic & AI providers
│   │   ├── models/              # Domain objects
│   │   ├── schemas/             # Pydantic DTOs
│   │   └── utils/               # Exceptions, helpers
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom hooks (useChat)
│   │   ├── styles/              # CSS files
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── .env.example
```

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/sessions` | Create session |
| GET | `/api/v1/sessions` | List sessions (paginated) |
| GET | `/api/v1/sessions/{id}` | Get session details |
| DELETE | `/api/v1/sessions/{id}` | Delete session |
| POST | `/api/v1/documents/upload` | Upload & parse document |
| GET | `/api/v1/documents` | List documents |
| POST | `/api/v1/messages` | Send message, get AI response |
| GET | `/api/v1/messages/{session_id}` | Get message history |

## Error Handling

Custom exception hierarchy:
- `SessionNotFoundError` (404)
- `DocumentNotFoundError` (404)
- `InvalidFileTypeError` (400)
- `FileTooLargeError` (413)
- `AIProviderError` (500)
- `AIRateLimitError` (429)

## Code Quality

- ✅ No errors or warnings
- ✅ Clean separation of concerns (frontend/backend)
- ✅ Async/await throughout
- ✅ Type hints on all functions
- ✅ Custom error handlers

## Next Steps

- [ ] Set up MongoDB Atlas M0 cluster
- [ ] Install Ollama for local AI testing
- [ ] Connect backend → MongoDB → Ollama
- [ ] Test full chat flow end-to-end
- [ ] Configure Hugging Face free API
- [ ] Deploy to AWS Lambda

## License

MIT