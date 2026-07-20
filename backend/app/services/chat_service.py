"""Chat service orchestration."""
from bson import ObjectId
from app.models.message import Message
from app.services.ai import get_ai_provider
from app.db.mongodb import get_database
from app.utils.exceptions import SessionNotFoundError, AIProviderError


async def send_chat_message(
    session_id: str,
    user_message: str,
) -> tuple[Message, Message]:
    """
    Send user message and get AI response.

    Args:
        session_id: Session ID
        user_message: User's message content

    Returns:
        Tuple of (user_message_doc, assistant_message_doc)

    Raises:
        SessionNotFoundError: If session doesn't exist
        AIProviderError: If AI call fails
    """
    db = get_database()
    session_oid = ObjectId(session_id)

    # Verify session exists
    session = await db.sessions.find_one({"_id": session_oid})
    if not session:
        raise SessionNotFoundError(session_id)

    # Store user message
    user_msg = Message(
        session_id=session_oid,
        role="user",
        content=user_message,
    )
    user_result = await db.messages.insert_one(user_msg.to_dict())
    user_msg._id = user_result.inserted_id

    # Get conversation history for context
    history = await db.messages.find({"session_id": session_oid}).to_list(None)
    messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history
    ]

    # Get document context if any
    document_context = None
    doc = await db.documents.find_one({"session_id": session_oid})
    if doc:
        # Truncate context if too large (keep first 4000 chars to stay within token limits)
        document_context = doc["extracted_text"][:4000]

    # Call AI provider
    ai_provider = get_ai_provider()
    ai_response = await ai_provider.chat(messages, context=document_context)

    # Store AI response
    assistant_msg = Message(
        session_id=session_oid,
        role="assistant",
        content=ai_response,
    )
    assistant_result = await db.messages.insert_one(assistant_msg.to_dict())
    assistant_msg._id = assistant_result.inserted_id

    # Update session's updated_at timestamp
    from datetime import datetime
    await db.sessions.update_one(
        {"_id": session_oid},
        {"$set": {"updated_at": datetime.utcnow()}},
    )

    return user_msg, assistant_msg
