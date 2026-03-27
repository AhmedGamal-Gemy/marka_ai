# Google ADK LLM Service Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the LLM service configuration and provider setup using the official Google Agent Development Kit (ADK), utilizing its built-in `LiteLlm` model wrapper for fallback/third-party model support, managed via `pydantic-settings`.

**Architecture:** 
1. **Enums (`AgentRole`)**: We will define roles (Orchestrator, Content, RAG, Chatbot) as an Enum to ensure type safety and eliminate magic strings.
2. **Configuration (`Settings`)**: A `pydantic-settings` class will read from `.env` and map `AgentRole`s to their specific model strings.
3. **Service Layer (`LLMService`)**: A central service that reads the configuration, ensures the necessary environment variables (`GEMINI_API_KEY`) are set for ADK/LiteLLM, and returns the correctly initialized ADK model instance (`LiteLlm` object).

**Tech Stack:** Python 3.12, FastAPI, Pydantic (pydantic-settings), Google ADK (`google-adk`), LiteLLM, pytest, pytest-asyncio

---

### Task 1: Create Enums and ADK-focused Configuration

**Files:**
- Create: `ai/app/models/enums.py`
- Modify: `ai/app/config.py`
- Create: `ai/tests/test_config.py`

- [ ] **Step 1: Write the failing test**

```python
# ai/tests/test_config.py
import os
from app.config import get_settings
from app.models.enums import AgentRole

def test_settings_loads_env_vars(monkeypatch):
    """Verify that pydantic-settings correctly loads from the environment."""
    monkeypatch.setenv("API_TOKEN", "test-token-123")
    monkeypatch.setenv("ORCHESTRATOR_MODEL", "gemini-3-flash")
    
    settings = get_settings()
    
    assert settings.API_TOKEN == "test-token-123"
    assert settings.get_model_for_role(AgentRole.ORCHESTRATOR) == "gemini-3-flash"
    assert settings.LLM_REQUESTS_PER_MINUTE == 25
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ai && uv add --dev pytest && uv run pytest tests/test_config.py -v && cd ..`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.models.enums'`

- [ ] **Step 3: Write the Enums and Configuration**

Create `ai/app/models/enums.py`:
```python
# ai/app/models/enums.py
from enum import Enum

class AgentRole(str, Enum):
    ORCHESTRATOR = "orchestrator"
    CONTENT = "content"
    RAG = "rag"
    CHATBOT = "chatbot"
    EMBEDDING = "embedding"
```

Modify `ai/app/config.py`:
```python
# ai/app/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.models.enums import AgentRole

class Settings(BaseSettings):
    """Core application settings for Marka AI."""
    API_TOKEN: str = "default-dev-token"
    LLM_API_KEY: str = ""

    # Smart Orchestrator Model Strategy
    ORCHESTRATOR_MODEL: str = "google/gemini-3-flash"
    CONTENT_MODEL: str = "google/gemini-3.1-pro"
    RAG_MODEL: str = "google/gemini-3.1-flash-lite"
    CHATBOT_MODEL: str = "google/gemini-3.1-flash-lite"
    EMBEDDING_MODEL: str = "google/gemini-embedding-2"
    
    QDRANT_VECTOR_SIZE: int = 768
    LLM_REQUESTS_PER_MINUTE: int = 25
    MAX_TOKENS_PER_REQUEST: int = 2000

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")

    def get_model_for_role(self, role: AgentRole) -> str:
        """Map the AgentRole enum to the configured model string."""
        mapping = {
            AgentRole.ORCHESTRATOR: self.ORCHESTRATOR_MODEL,
            AgentRole.CONTENT: self.CONTENT_MODEL,
            AgentRole.RAG: self.RAG_MODEL,
            AgentRole.CHATBOT: self.CHATBOT_MODEL,
            AgentRole.EMBEDDING: self.EMBEDDING_MODEL,
        }
        return mapping[role]

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ai && uv run pytest tests/test_config.py -v && cd ..`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ai/app/models/enums.py ai/app/config.py ai/tests/test_config.py
git commit -m "feat(ai): define AgentRole enum and configure pydantic-settings for ADK"
```

### Task 2: Create the ADK LLM Service

**Files:**
- Create: `ai/app/services/llm_service.py`
- Create: `ai/tests/test_llm_service.py`

- [ ] **Step 1: Write the failing test**

```python
# ai/tests/test_llm_service.py
import os
import pytest
from app.services.llm_service import LLMService
from app.models.enums import AgentRole

def test_llm_service_initialization():
    """Verify the service sets the necessary environment variables for ADK/LiteLLM."""
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("OPENAI_API_KEY", None) # In case config loads a generic one
    
    service = LLMService()
    
    # ADK's LiteLlm wrapper requires GEMINI_API_KEY for Google models
    assert "GEMINI_API_KEY" in os.environ
    assert service.settings is not None

def test_get_adk_model():
    """Verify the service returns a correctly configured ADK LiteLlm model."""
    service = LLMService()
    # The ADK LiteLlm class has a 'model' attribute containing the string name
    adk_model = service.get_adk_model(AgentRole.ORCHESTRATOR)
    
    # It should resolve to the config default: google/gemini-3-flash
    assert adk_model.model == "google/gemini-3-flash"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ai && uv add google-adk litellm && uv run pytest tests/test_llm_service.py -v && cd ..`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.services.llm_service'`

- [ ] **Step 3: Write minimal implementation**

Create `ai/app/services/llm_service.py`:
```python
# ai/app/services/llm_service.py
import os
from google.adk.models.lite_llm import LiteLlm
from app.config import get_settings
from app.models.enums import AgentRole

class LLMService:
    """
    Provides initialized Google ADK models for Marka AI agents.
    Utilizes ADK's native LiteLlm wrapper to support Google models 
    as well as fallback providers (Mistral, Groq) seamlessly.
    """
    def __init__(self):
        self.settings = get_settings()
        self._ensure_environment_keys()

    def _ensure_environment_keys(self):
        """
        ADK and LiteLLM rely heavily on environment variables.
        We ensure our centralized config is pushed to os.environ 
        so ADK can pick it up natively.
        """
        if self.settings.LLM_API_KEY:
             # Standard fallback keys LiteLLM looks for
             os.environ["GEMINI_API_KEY"] = self.settings.LLM_API_KEY
             os.environ["GOOGLE_API_KEY"] = self.settings.LLM_API_KEY
             
             # If using Groq/Mistral later, we can map them here from settings
             # os.environ["GROQ_API_KEY"] = self.settings.GROQ_API_KEY

    def get_adk_model(self, role: AgentRole) -> LiteLlm:
        """
        Returns a fully initialized ADK model instance ready to be 
        passed into `google.adk.agents.Agent(model=...)`.
        """
        model_name = self.settings.get_model_for_role(role)
        
        # ADK's LiteLlm handles the provider/model string natively
        return LiteLlm(model=model_name)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ai && uv run pytest tests/test_llm_service.py -v && cd ..`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ai/pyproject.toml ai/uv.lock ai/app/services/llm_service.py ai/tests/test_llm_service.py
git commit -m "feat(ai): create LLMService returning native ADK LiteLlm models based on roles"
```