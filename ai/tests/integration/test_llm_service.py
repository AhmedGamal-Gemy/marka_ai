import os
import pytest
from typing import Union
from app.services.llm_service import LLMService
from app.models.enums import AgentRole
from google.adk.models import Gemini, LiteLlm
from app.config import get_settings, Settings

def test_llm_service_initialization_uses_settings_object(settings):
    """Verifies that LLMService correctly uses the provided settings object."""
    service = LLMService(settings=settings)
    assert service.settings == settings

def test_llm_service_initialization_with_custom_settings():
    """Verifies that LLMService can be initialized with custom settings."""
    custom_settings = Settings(LLM_API_KEY="custom-test-key")
    service = LLMService(settings=custom_settings)
    assert service.settings.LLM_API_KEY == "custom-test-key"
    assert service.settings == custom_settings

def test_get_adk_model_returns_correct_gemini_object(settings):
    """Verifies that get_adk_model returns a Gemini instance for Google models."""
    service = LLMService(settings=settings)
    
    # ORCHESTRATOR_MODEL defaults to "gemini/..." in Settings
    model = service.get_adk_model(AgentRole.ORCHESTRATOR)
    
    assert isinstance(model, Gemini)
    # The clean name should be the last part of the slash-separated string
    expected_model = settings.ORCHESTRATOR_MODEL.split("/")[-1]
    assert model.model == expected_model

def test_get_adk_model_returns_correct_litellm_object():
    """Verifies that get_adk_model returns a LiteLlm instance for non-Google models."""
    custom_settings = Settings(ORCHESTRATOR_MODEL="gpt-4o")
    service = LLMService(settings=custom_settings)
    
    model = service.get_adk_model(AgentRole.ORCHESTRATOR)
    
    assert isinstance(model, LiteLlm)
    assert model.model == "gpt-4o"
