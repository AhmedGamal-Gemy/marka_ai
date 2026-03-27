import os
import pytest
from app.services.llm_service import LLMService
from app.models.enums import AgentRole
from google.adk.models.lite_llm import LiteLlm
from app.config import get_settings

def test_llm_service_initialization_injects_env_vars():
    # Store original env vars
    original_gemini = os.environ.get("GEMINI_API_KEY")
    original_google = os.environ.get("GOOGLE_API_KEY")
    
    try:
        # Clear existing env vars
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
        if "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]
            
        settings = get_settings()
        # Mocking settings if possible, or just trust the current environment
        # but let's assume we can set LLM_API_KEY
        settings.LLM_API_KEY = "test-api-key"
        
        service = LLMService()
        
        assert os.environ["GEMINI_API_KEY"] == settings.LLM_API_KEY
        assert os.environ["GOOGLE_API_KEY"] == settings.LLM_API_KEY
    finally:
        # Restore original env vars
        if original_gemini:
            os.environ["GEMINI_API_KEY"] = original_gemini
        if original_google:
            os.environ["GOOGLE_API_KEY"] = original_google

def test_get_adk_model_returns_correct_litellm_object():
    service = LLMService()
    settings = get_settings()
    
    model = service.get_adk_model(AgentRole.ORCHESTRATOR)
    
    assert isinstance(model, LiteLlm)
    assert model.model == settings.ORCHESTRATOR_MODEL
