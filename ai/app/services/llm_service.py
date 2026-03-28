import os
from typing import Optional
from app.config import get_settings, Settings
from app.models.enums import AgentRole
from google.adk.models.lite_llm import LiteLlm

class LLMService:
    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()
        
    def get_adk_model(self, role: AgentRole) -> LiteLlm:
        """
        Returns a configured LiteLlm model for the specified AgentRole.
        """
        model_name = self.settings.get_model_for_role(role)
        return LiteLlm(model=model_name, api_key=self.settings.LLM_API_KEY)
