"""AI provider factory."""
from app.core.config import settings
from app.services.ai.base import AIProvider
from app.services.ai.ollama_provider import OllamaProvider
from app.services.ai.huggingface_provider import HuggingFaceProvider


def get_ai_provider() -> AIProvider:
    """Get configured AI provider."""
    if settings.ai_provider == "ollama":
        return OllamaProvider(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )
    elif settings.ai_provider == "huggingface":
        return HuggingFaceProvider(
            api_key=settings.huggingface_api_key,
            model=settings.huggingface_model,
        )
    else:
        raise ValueError(f"Unknown AI provider: {settings.ai_provider}")
