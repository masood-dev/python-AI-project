"""Message domain model."""
from datetime import datetime
from bson import ObjectId


class Message:
    """Represents a chat message."""

    def __init__(
        self,
        session_id: ObjectId,
        role: str,  # "user" or "assistant"
        content: str,
        created_at: datetime | None = None,
        _id: ObjectId | None = None,
    ):
        """Initialize message."""
        self._id = _id or ObjectId()
        self.session_id = session_id
        self.role = role
        self.content = content
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert to dict for MongoDB storage."""
        return {
            "_id": self._id,
            "session_id": self.session_id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        """Create from MongoDB dict."""
        return cls(
            session_id=data["session_id"],
            role=data["role"],
            content=data["content"],
            created_at=data.get("created_at"),
            _id=data.get("_id"),
        )
