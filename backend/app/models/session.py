"""Session domain model."""
from datetime import datetime
from bson import ObjectId


class Session:
    """Represents a chat session."""

    def __init__(
        self,
        title: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        _id: ObjectId | None = None,
    ):
        """Initialize session."""
        self._id = _id or ObjectId()
        self.title = title
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert to dict for MongoDB storage."""
        return {
            "_id": self._id,
            "title": self.title,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        """Create from MongoDB dict."""
        return cls(
            title=data["title"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            _id=data.get("_id"),
        )
