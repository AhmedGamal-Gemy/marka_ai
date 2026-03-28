import os
import pytest
from app.services.llm_service import LLMService
from app.models.enums import AgentRole
from google.adk.models.lite_llm import LiteLlm
from app.config import get_settings

def test_llm_service_initialization_uses_settings_object(settings):
    service = LLMService(settings=settings)
    assert service.settings == settings

def test_llm_service_initialization_with_custom_settings():
    from app.config import Settings
    custom_settings = Settings(LLM_API_KEY="custom-test-key")
    service = LLMService(settings=custom_settings)
    assert service.settings.LLM_API_KEY == "custom-test-key"
    assert service.settings == custom_settings

def test_get_adk_model_returns_correct_litellm_object(settings):
    service = LLMService(settings=settings)
    
    model = service.get_adk_model(AgentRole.ORCHESTRATOR)
    
    assert isinstance(model, LiteLlm)
    assert model.model == settings.ORCHESTRATOR_MODEL
