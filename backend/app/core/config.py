"""Application configuration from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # App
    app_name: str = "StudyChat AI"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db: str = "studychat"

    # AI Provider
    ai_provider: str = "ollama"  # "ollama" or "huggingface"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    huggingface_api_key: str = ""
    huggingface_model: str = "meta-llama/Llama-2-7b-chat-hf"

    # File upload
    max_file_size_mb: int = 50
    allowed_file_types: list[str] = ["pdf", "docx", "txt"]

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


settings = Settings()
