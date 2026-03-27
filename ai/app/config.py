import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.models.enums import AgentRole

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
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
    return Settings()
