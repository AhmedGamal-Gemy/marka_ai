import os
from app.config import get_settings
from app.models.enums import AgentRole
from google.adk.models.lite_llm import LiteLlm

class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()
        os.environ["GEMINI_API_KEY"] = self.settings.LLM_API_KEY
        os.environ["GOOGLE_API_KEY"] = self.settings.LLM_API_KEY
        
    def get_adk_model(self, role: AgentRole) -> LiteLlm:
        """
        Returns a configured LiteLlm model for the specified AgentRole.
        """
        model_name = self.settings.get_model_for_role(role)
        return LiteLlm(model=model_name)
