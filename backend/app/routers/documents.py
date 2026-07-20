"""Document management routes."""
from fastapi import APIRouter, File, UploadFile, status, Response
from bson import ObjectId
from app.schemas.document_schemas import DocumentResponse, DocumentListResponse
from app.services.document_service import parse_and_store_document
from app.db.mongodb import get_database
from app.utils.exceptions import SessionNotFoundError

router = APIRouter(prefix="/api/v1/sessions", tags=["documents"])


@router.post(
    "/{session_id}/documents",
    status_code=status.HTTP_201_CREATED,
    response_model=DocumentResponse,
)
async def upload_document(session_id: str, file: UploadFile = File(...), response: Response = None):
    """Upload and parse a document for a session."""
    db = get_database()

    try:
        session_oid = ObjectId(session_id)
    except Exception:
        raise SessionNotFoundError(session_id)

    # Verify session exists
    session = await db.sessions.find_one({"_id": session_oid})
    if not session:
        raise SessionNotFoundError(session_id)

    # Get file extension
    filename = file.filename or "unknown"
    file_type = filename.split(".")[-1] if "." in filename else ""

    # Read file content
    file_bytes = await file.read()

    # Parse and store
    document = await parse_and_store_document(
        session_id=session_oid,
        filename=filename,
        file_bytes=file_bytes,
        file_type=file_type,
    )

    response.headers["Location"] = f"/api/v1/documents/{document._id}"

    return DocumentResponse(
        _id=str(document._id),
        session_id=str(document.session_id),
        filename=document.filename,
        file_type=document.file_type,
        uploaded_at=document.uploaded_at,
    )


@router.get("/{session_id}/documents", response_model=DocumentListResponse)
async def list_documents(session_id: str):
    """List documents in a session."""
    db = get_database()

    try:
        session_oid = ObjectId(session_id)
    except Exception:
        raise SessionNotFoundError(session_id)

    # Verify session exists
    session = await db.sessions.find_one({"_id": session_oid})
    if not session:
        raise SessionNotFoundError(session_id)

    documents = await db.documents.find({"session_id": session_oid}).to_list(None)

    return DocumentListResponse(
        documents=[
            DocumentResponse(
                _id=str(d["_id"]),
                session_id=str(d["session_id"]),
                filename=d["filename"],
                file_type=d["file_type"],
                uploaded_at=d["uploaded_at"],
            )
            for d in documents
        ],
        total=len(documents),
    )
