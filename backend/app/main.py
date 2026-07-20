"""FastAPI application factory and setup."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.mongodb import connect_db, disconnect_db
from app.utils.exceptions import AppException, app_exception_handler
from app.routers import sessions, documents, messages


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Manage app lifecycle (startup and shutdown)."""
    # Startup
    await connect_db()
    yield
    # Shutdown
    await disconnect_db()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="StudyChat AI",
        description="Chat-based study assistant",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handler
    app.add_exception_handler(AppException, app_exception_handler)

    # Routes
    app.include_router(sessions.router)
    app.include_router(documents.router)
    app.include_router(messages.router)

    @app.get("/health", tags=["health"])
    async def health():
        """Health check endpoint."""
        return {"status": "ok"}

    return app


app = create_app()
