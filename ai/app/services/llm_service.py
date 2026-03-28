from typing import Union, Optional
from app.config import get_settings, Settings
from app.models.enums import AgentRole
from google.adk.models import Gemini, LiteLlm

class LLMService:
    """Central provider for Large Language Model (LLM) instances across the application.

    This service is responsible for providing correctly configured LLM instances
    based on the requested AgentRole and the application's configuration. It
    abstracts the selection logic between native Gemini implementations and
    the LiteLlm fallback wrapper, ensuring optimal tool and schema support
    when possible.
    """

    def __init__(self, settings: Optional[Settings] = None) -> None:
        """Initializes the LLMService.

        Args:
            settings: An optional Settings object. If not provided, it will be
                retrieved using the get_settings() utility.
        """
        self.settings = settings or get_settings()
        
    def get_adk_model(self, role: AgentRole) -> Union[Gemini, LiteLlm]:
        """Retrieves a configured ADK model instance for a specified role.

        This method selects the appropriate model class (Gemini or LiteLlm)
        based on the model name configured for the given role. It prioritizes
        the native Gemini class for Google models for enhanced tool/schema
        support, while falling back to LiteLlm for other providers.

        Args:
            role: The AgentRole for which to retrieve the model.

        Returns:
            A configured instance of either Gemini or LiteLlm.
        """
        model_name = self.settings.get_model_for_role(role)
        
        # If it's a gemini model, use the native ADK Gemini class for better tool support
        if "gemini" in model_name.lower():
            # Strip prefixes like 'gemini/' or 'google/' if present to ensure
            # compatibility with the ADK model parameter.
            clean_name = model_name.split("/")[-1]
            return Gemini(model=clean_name, api_key=self.settings.LLM_API_KEY)
            
        # For non-Google models, fallback to LiteLlm wrapper for multi-provider support
        return LiteLlm(model=model_name, api_key=self.settings.LLM_API_KEY)
