"""Message and chat routes."""
from fastapi import APIRouter, status
from bson import ObjectId
from app.schemas.message_schemas import (
    MessageCreate,
    MessageResponse,
    MessageListResponse,
    ChatResponse,
)
from app.services.chat_service import send_chat_message
from app.db.mongodb import get_database
from app.utils.exceptions import SessionNotFoundError

router = APIRouter(prefix="/api/v1/sessions", tags=["messages"])


@router.post(
    "/{session_id}/messages",
    status_code=status.HTTP_201_CREATED,
    response_model=ChatResponse,
)
async def chat(session_id: str, req: MessageCreate):
    """Send a chat message and get AI response."""
    user_msg, assistant_msg = await send_chat_message(session_id, req.content)

    return ChatResponse(
        user_message=MessageResponse(
            _id=str(user_msg._id),
            session_id=str(user_msg.session_id),
            role=user_msg.role,
            content=user_msg.content,
            created_at=user_msg.created_at,
        ),
        assistant_message=MessageResponse(
            _id=str(assistant_msg._id),
            session_id=str(assistant_msg.session_id),
            role=assistant_msg.role,
            content=assistant_msg.content,
            created_at=assistant_msg.created_at,
        ),
    )


@router.get("/{session_id}/messages", response_model=MessageListResponse)
async def get_messages(session_id: str):
    """Get all messages in a session."""
    db = get_database()

    try:
        session_oid = ObjectId(session_id)
    except Exception:
        raise SessionNotFoundError(session_id)

    # Verify session exists
    session = await db.sessions.find_one({"_id": session_oid})
    if not session:
        raise SessionNotFoundError(session_id)

    messages = await db.messages.find({"session_id": session_oid}).to_list(None)

    return MessageListResponse(
        messages=[
            MessageResponse(
                _id=str(m["_id"]),
                session_id=str(m["session_id"]),
                role=m["role"],
                content=m["content"],
                created_at=m["created_at"],
            )
            for m in messages
        ],
        total=len(messages),
    )
