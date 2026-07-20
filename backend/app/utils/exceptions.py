"""Custom exception classes and error handlers."""
from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str | None = None,
    ):
        """Initialize exception."""
        self.message = message
        self.status_code = status_code
        self.detail = detail or message
        super().__init__(self.message)


class SessionNotFoundError(AppException):
    """Session not found."""

    def __init__(self, session_id: str):
        """Initialize exception."""
        super().__init__(
            f"Session {session_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class DocumentNotFoundError(AppException):
    """Document not found."""

    def __init__(self, document_id: str):
        """Initialize exception."""
        super().__init__(
            f"Document {document_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class InvalidFileTypeError(AppException):
    """Invalid file type uploaded."""

    def __init__(self, file_type: str, allowed_types: list[str]):
        """Initialize exception."""
        super().__init__(
            f"File type '{file_type}' not allowed. Allowed: {', '.join(allowed_types)}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class FileTooLargeError(AppException):
    """File exceeds size limit."""

    def __init__(self, size_mb: int, max_mb: int):
        """Initialize exception."""
        super().__init__(
            f"File size {size_mb}MB exceeds limit of {max_mb}MB",
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        )


class DocumentParsingError(AppException):
    """Failure to parse document."""

    def __init__(self, filename: str, reason: str):
        """Initialize exception."""
        super().__init__(
            f"Failed to parse {filename}: {reason}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class AIProviderError(AppException):
    """AI provider returned error or is unavailable."""

    def __init__(self, reason: str):
        """Initialize exception."""
        super().__init__(
            f"AI provider error: {reason}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


class AIRateLimitError(AppException):
    """AI provider rate limited."""

    def __init__(self):
        """Initialize exception."""
        super().__init__(
            "AI service is rate limited. Please try again in a moment.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )


async def app_exception_handler(request: Request, exc: AppException):  # noqa: ARG001
    """Handle application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "detail": exc.detail,
        },
    )
