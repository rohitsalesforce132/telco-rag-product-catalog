"""Model router for query-based model selection."""
from typing import Literal
from .config import settings


class ModelRouter:
    """
    Route queries to optimal model based on intent and complexity.
    Saves 60% on LLM costs by using cheaper models for simple queries.
    """

    MODEL_MAPPING = {
        "haiku": "claude-3-5-haiku-20241022",
        "sonnet": "claude-3-5-sonnet-20241022",
        "opus": "claude-3-5-opus-20241022"
    }

    def route(self, intent: str, query: str) -> Literal["haiku", "sonnet", "opus"]:
        """
        Route to optimal model.

        Routing strategy:
        - Haiku: Simple product lookups, short queries (<50 tokens)
        - Sonnet: Order validation, troubleshooting, medium complexity
        - Opus: Complex recommendations, multi-step reasoning
        """
        query_length = len(query.split())

        # Route by intent
        if intent == "search" and query_length < 50:
            return "haiku"
        elif intent == "search" or intent == "validate":
            return "sonnet"
        elif intent == "recommend":
            # For recommendations, check complexity
            if query_length > 100:
                return "opus"
            return "sonnet"
        elif intent == "troubleshoot":
            # Troubleshooting is usually complex
            return "sonnet"
        else:
            # Default to sonnet
            return "sonnet"

    def get_model_name(self, model: str) -> str:
        """Map model code to Claude model name."""
        return self.MODEL_MAPPING.get(model, self.MODEL_MAPPING["sonnet"])
