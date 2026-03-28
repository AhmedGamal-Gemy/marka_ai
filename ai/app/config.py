import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.models.enums import AgentRole

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    """Application configuration settings for the Marka AI framework.

    This class manages environment variables, model selection, and general
    operational limits for the Core AI layer. It uses Pydantic Settings
    to automatically load configuration from environment variables or a .env file.

    Attributes:
        API_TOKEN (str): Internal API token for authentication between services.
        LLM_API_KEY (str): API key for LLM provider (e.g., Google Gemini).
        ORCHESTRATOR_MODEL (str): Model used by the orchestrator agent.
        CONTENT_MODEL (str): Model used for generating marketing content.
        RAG_MODEL (str): Model used for Retrieval-Augmented Generation.
        CHATBOT_MODEL (str): Model used for conversational interactions.
        EMBEDDING_MODEL (str): Model used for generating vector embeddings.
        LLM_REQUESTS_PER_MINUTE (int): Rate limiting threshold for LLM requests.
        model_config (SettingsConfigDict): Configuration for environment file loading.
    """
    
    API_TOKEN: str = ""
    LLM_API_KEY: str = ""
    
    # Model variables matching `.env.example`
    ORCHESTRATOR_MODEL: str = "gemini/gemini-3-flash-preview"
    CONTENT_MODEL: str = "gemini/gemini-3.1-pro-preview"
    RAG_MODEL: str = "gemini/gemini-3.1-flash-lite-preview"
    CHATBOT_MODEL: str = "gemini/gemini-3.1-flash-lite-preview"
    EMBEDDING_MODEL: str = "gemini/gemini-embedding-2"
    
    LLM_REQUESTS_PER_MINUTE: int = 25

    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def get_model_for_role(self, role: AgentRole) -> str:
        """Retrieves the assigned model for a specific agent role.

        Args:
            role (AgentRole): The functional role of the agent.

        Returns:
            str: The model identifier string for the given role.

        Raises:
            ValueError: If the provided role is not recognized.
        """
        if role == AgentRole.ORCHESTRATOR:
            return self.ORCHESTRATOR_MODEL
        elif role == AgentRole.CONTENT:
            return self.CONTENT_MODEL
        elif role == AgentRole.RAG:
            return self.RAG_MODEL
        elif role == AgentRole.CHATBOT:
            return self.CHATBOT_MODEL
        elif role == AgentRole.EMBEDDING:
            return self.EMBEDDING_MODEL
        else:
            raise ValueError(f"Unknown role: {role}")

@lru_cache()
def get_settings() -> Settings:
    """Provides a singleton-like cached instance of the application settings.

    Returns:
        Settings: The application configuration object.
    """
    return Settings()
