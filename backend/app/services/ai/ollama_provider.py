"""Ollama AI provider."""
import httpx
from app.services.ai.base import AIProvider
from app.utils.exceptions import AIProviderError


class OllamaProvider(AIProvider):
    """Local Ollama provider."""

    def __init__(self, base_url: str, model: str):
        """Initialize Ollama provider."""
        self.base_url = base_url
        self.model = model

    async def chat(self, messages: list[dict], context: str | None = None) -> str:
        """Send chat request to Ollama."""
        # Inject context if provided
        system_message = {
            "role": "system",
            "content": f"You are a helpful study assistant. {f'Reference document: {context}' if context else ''}",
        }

        payload = {
            "model": self.model,
            "messages": [system_message] + messages,
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "")
        except httpx.HTTPStatusError as e:
            raise AIProviderError(f"Ollama error: {e.response.text}")
        except Exception as e:
            raise AIProviderError(f"Failed to connect to Ollama: {str(e)}")
