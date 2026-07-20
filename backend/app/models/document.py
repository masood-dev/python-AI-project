"""Document domain model."""
from datetime import datetime
from bson import ObjectId


class Document:
    """Represents an uploaded document."""

    def __init__(
        self,
        session_id: ObjectId,
        filename: str,
        file_type: str,  # "pdf", "docx", or "txt"
        extracted_text: str,
        uploaded_at: datetime | None = None,
        _id: ObjectId | None = None,
    ):
        """Initialize document."""
        self._id = _id or ObjectId()
        self.session_id = session_id
        self.filename = filename
        self.file_type = file_type
        self.extracted_text = extracted_text
        self.uploaded_at = uploaded_at or datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert to dict for MongoDB storage."""
        return {
            "_id": self._id,
            "session_id": self.session_id,
            "filename": self.filename,
            "file_type": self.file_type,
            "extracted_text": self.extracted_text,
            "uploaded_at": self.uploaded_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Document":
        """Create from MongoDB dict."""
        return cls(
            session_id=data["session_id"],
            filename=data["filename"],
            file_type=data["file_type"],
            extracted_text=data["extracted_text"],
            uploaded_at=data.get("uploaded_at"),
            _id=data.get("_id"),
        )
