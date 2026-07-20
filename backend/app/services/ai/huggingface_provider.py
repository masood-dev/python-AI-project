"""Hugging Face AI provider."""
import httpx
from app.services.ai.base import AIProvider
from app.utils.exceptions import AIProviderError, AIRateLimitError


class HuggingFaceProvider(AIProvider):
    """Hugging Face Inference API provider."""

    def __init__(self, api_key: str, model: str):
        """Initialize Hugging Face provider."""
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api-inference.huggingface.co/models"

    async def chat(self, messages: list[dict], context: str | None = None) -> str:
        """Send chat request to Hugging Face."""
        if not self.api_key:
            raise AIProviderError("Hugging Face API key not configured")

        # Format messages as conversation
        conversation = ""
        for msg in messages:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")
            conversation += f"{role}: {content}\n"

        if context:
            conversation = f"Context: {context}\n\n{conversation}"

        prompt = conversation + "Assistant:"

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
            },
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/{self.model}",
                    json=payload,
                    headers=headers,
                )

                if response.status_code == 429:
                    raise AIRateLimitError()

                response.raise_for_status()
                data = response.json()

                # Handle both single response and list responses
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get("generated_text", "").strip()
                elif isinstance(data, dict):
                    return data.get("generated_text", "").strip()

                raise AIProviderError("Unexpected response format from Hugging Face")

        except AIRateLimitError:
            raise
        except httpx.HTTPStatusError as e:
            raise AIProviderError(f"Hugging Face error: {e.response.text}")
        except Exception as e:
            raise AIProviderError(f"Failed to call Hugging Face: {str(e)}")
