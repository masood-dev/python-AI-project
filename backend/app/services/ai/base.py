"""Abstract base class for AI providers."""
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract interface for AI providers."""

    @abstractmethod
    async def chat(self, messages: list[dict], context: str | None = None) -> str:
        """
        Send messages to the AI and get a response.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
            context: Optional document context for the conversation

        Returns:
            String response from the AI

        Raises:
            AIProviderError: If the provider fails
            AIRateLimitError: If rate-limited (429)
        """
        pass
