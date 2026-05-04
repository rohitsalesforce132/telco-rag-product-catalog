"""Configuration management for Telco RAG Product Catalog."""
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings."""

    # Anthropic API
    anthropic_api_key: str

    # OpenAI API (for embeddings)
    openai_api_key: str

    # Neo4j (Knowledge Graph)
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str

    # Qdrant (Vector DB)
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""

    # PostgreSQL (Metadata Store)
    postgres_uri: str = "postgresql://user:password@localhost:5432/telco_catalog"

    # Redis (Cache)
    redis_url: str = "redis://localhost:6379"

    # TMF APIs
    tmf620_base_url: str
    tmf622_base_url: str
    tmf_api_key: str

    # Supporting APIs
    inventory_api_url: str
    pricing_api_url: str
    customer_api_url: str

    # Observability
    jaeger_host: str = "jaeger"
    jaeger_port: int = 6831
    prometheus_port: int = 9090

    # Application
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    max_retries: int = 3
    timeout_seconds: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
