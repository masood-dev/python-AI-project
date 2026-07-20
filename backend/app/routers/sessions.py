"""Session management routes."""
from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from bson import ObjectId
from app.schemas.session_schemas import (
    SessionCreate,
    SessionResponse,
    SessionListResponse,
)
from app.db.mongodb import get_database
from app.models.session import Session
from app.utils.exceptions import SessionNotFoundError

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SessionResponse)
async def create_session(req: SessionCreate, response: Response):
    """Create a new chat session."""
    db = get_database()

    session = Session(title=req.title)
    result = await db.sessions.insert_one(session.to_dict())
    session._id = result.inserted_id

    response.headers["Location"] = f"/api/v1/sessions/{session._id}"

    return SessionResponse(
        _id=str(session._id),
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
    )


@router.get("", response_model=SessionListResponse)
async def list_sessions(page: int = 1, page_size: int = 20):
    """List all sessions (paginated)."""
    db = get_database()

    if page < 1 or page_size < 1:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "page and page_size must be >= 1"},
        )

    skip = (page - 1) * page_size
    sessions = await db.sessions.find().skip(skip).limit(page_size).to_list(None)
    total = await db.sessions.count_documents({})

    return SessionListResponse(
        sessions=[
            SessionResponse(
                _id=str(s["_id"]),
                title=s["title"],
                created_at=s["created_at"],
                updated_at=s["updated_at"],
            )
            for s in sessions
        ],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """Get a session by ID."""
    db = get_database()

    try:
        oid = ObjectId(session_id)
    except Exception:
        raise SessionNotFoundError(session_id)

    session = await db.sessions.find_one({"_id": oid})
    if not session:
        raise SessionNotFoundError(session_id)

    return SessionResponse(
        _id=str(session["_id"]),
        title=session["title"],
        created_at=session["created_at"],
        updated_at=session["updated_at"],
    )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str):
    """Delete a session and all its data."""
    db = get_database()

    try:
        oid = ObjectId(session_id)
    except Exception:
        raise SessionNotFoundError(session_id)

    session = await db.sessions.find_one({"_id": oid})
    if not session:
        raise SessionNotFoundError(session_id)

    # Delete all related data
    await db.messages.delete_many({"session_id": oid})
    await db.documents.delete_many({"session_id": oid})
    await db.sessions.delete_one({"_id": oid})

    return None
