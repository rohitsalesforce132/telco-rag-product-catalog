"""Query intent classifier using Claude Haiku."""
from typing import Literal
from anthropic import Anthropic
from .config import settings


class IntentClassifier:
    """Classify user query intent."""

    VALID_INTENTS = ["search", "validate", "recommend", "troubleshoot"]

    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)

    async def classify(self, query: str) -> Literal["search", "validate", "recommend", "troubleshoot"]:
        """
        Classify query intent.

        Args:
            query: Natural language query

        Returns:
            Intent classification
        """
        prompt = f"""
        Classify the following query into one of these intents:
        - search: User wants to find products
        - validate: User wants to validate an order
        - recommend: User wants product recommendations
        - troubleshoot: User wants help with a failed order

        Query: {query}

        Return only the intent name (search, validate, recommend, or troubleshoot).
        """

        try:
            response = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=10,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )

            intent = response.content[0].text.strip().lower()

            # Validate intent
            if intent not in self.VALID_INTENTS:
                # Default to search if unknown
                return "search"

            return intent

        except Exception as e:
            # Fallback to simple keyword matching
            query_lower = query.lower()

            if any(word in query_lower for word in ["validate", "check", "verify"]):
                return "validate"
            elif any(word in query_lower for word in ["recommend", "suggest", "best"]):
                return "recommend"
            elif any(word in query_lower for word in ["troubleshoot", "error", "failed", "problem"]):
                return "troubleshoot"
            else:
                return "search"
