# StudyChat AI - Updated Project Brief

## No Flashcards - Pure Text-Based Chat

StudyChat AI is now a simplified chat-based study assistant styled like ChatGPT/Gemini. Students upload documents (PDF, DOCX, TXT), converse with an AI about the content, and receive text-only responses.

### Simplified Data Model

**sessions collection**
```json
{
  "_id": "ObjectId",
  "title": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**documents collection**
```json
{
  "_id": "ObjectId",
  "session_id": "ObjectId (ref sessions)",
  "filename": "string",
  "file_type": "pdf | docx | txt",
  "extracted_text": "string",
  "uploaded_at": "datetime"
}
```

**messages collection** (text-only)
```json
{
  "_id": "ObjectId",
  "session_id": "ObjectId (ref sessions)",
  "role": "user | assistant",
  "content": "string",
  "created_at": "datetime"
}
```

### Simplified REST API

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/sessions` | Create a new chat session |
| GET | `/api/v1/sessions` | List all sessions (paginated) |
| GET | `/api/v1/sessions/{session_id}` | Get one session's metadata |
| DELETE | `/api/v1/sessions/{session_id}` | Delete a session and its data |
| POST | `/api/v1/sessions/{session_id}/documents` | Upload + parse a document |
| GET | `/api/v1/sessions/{session_id}/documents` | List documents in a session |
| POST | `/api/v1/sessions/{session_id}/messages` | Send a chat message, get AI reply |
| GET | `/api/v1/sessions/{session_id}/messages` | Get full message history |

### Frontend Components (Simplified)

- **ChatWindow** — top-level container
- **Sidebar** — list of past sessions, "New Chat" button
- **MessageList** — scrollable list of message bubbles
- **MessageBubble** — renders text only (user or assistant)
- **ChatInput** — text input + file upload button

No flashcard widget. No interactive inline content. Pure text conversation.

### Tech Stack (Unchanged)

- **Frontend**: React 18 + Vite, plain CSS or Tailwind
- **Backend**: Python 3.11+, FastAPI
- **Database**: MongoDB Atlas (M0)
- **AI (dev)**: Ollama + llama3.2:3b or phi3:mini
- **AI (prod)**: Hugging Face Inference API
- **Deployment**: AWS Lambda + S3 + CloudFront
- **CI/CD**: GitHub Actions

All free-tier constraints remain in effect.
