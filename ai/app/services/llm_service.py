import os
from typing import Optional
from app.config import get_settings, Settings
from app.models.enums import AgentRole
from google.adk.models import Gemini, LiteLlm

class LLMService:
    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()
        
    def get_adk_model(self, role: AgentRole) -> Gemini | LiteLlm:
        """
        Returns a configured model instance for the specified AgentRole.
        Uses native Gemini class for Google models for better tool/schema support.
        """
        model_name = self.settings.get_model_for_role(role)
        
        # If it's a gemini model, use the native ADK Gemini class
        if "gemini" in model_name.lower():
            # Strip prefixes like 'gemini/' or 'google/' if present
            clean_name = model_name.split("/")[-1]
            return Gemini(model=clean_name, api_key=self.settings.LLM_API_KEY)
            
        # For non-Google models, fallback to LiteLlm wrapper
        return LiteLlm(model=model_name, api_key=self.settings.LLM_API_KEY)
