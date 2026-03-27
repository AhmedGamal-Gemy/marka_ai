import os
import pytest
from pydantic_settings import BaseSettings

from app.config import get_settings
from app.models.enums import AgentRole

@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield

def test_settings_loads_env_vars(monkeypatch):
    """Verify that pydantic-settings correctly loads from the environment."""
    monkeypatch.setenv("API_TOKEN", "test-token-123")
    monkeypatch.setenv("LLM_API_KEY", "test-key-456")
    monkeypatch.setenv("ORCHESTRATOR_MODEL", "test/orchestrator-model")
    monkeypatch.setenv("CONTENT_MODEL", "test/content-model")
    monkeypatch.setenv("RAG_MODEL", "test/rag-model")
    monkeypatch.setenv("CHATBOT_MODEL", "test/chatbot-model")
    monkeypatch.setenv("EMBEDDING_MODEL", "test/embedding-model")
    monkeypatch.setenv("LLM_REQUESTS_PER_MINUTE", "50")

    settings = get_settings()

    assert settings.API_TOKEN == "test-token-123"
    assert settings.LLM_API_KEY == "test-key-456"
    assert settings.get_model_for_role(AgentRole.ORCHESTRATOR) == "test/orchestrator-model"
    assert settings.get_model_for_role(AgentRole.CONTENT) == "test/content-model"
    assert settings.get_model_for_role(AgentRole.RAG) == "test/rag-model"
    assert settings.get_model_for_role(AgentRole.CHATBOT) == "test/chatbot-model"
    assert settings.get_model_for_role(AgentRole.EMBEDDING) == "test/embedding-model"
    assert settings.LLM_REQUESTS_PER_MINUTE == 50

def test_get_model_for_role_invalid():
    """Verify that invalid roles raise an error."""
    settings = get_settings()
    with pytest.raises(ValueError):
        settings.get_model_for_role("invalid-role")
