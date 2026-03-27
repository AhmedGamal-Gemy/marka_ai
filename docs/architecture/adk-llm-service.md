# LLM Service & ADK Integration

This document outlines the architecture and implementation details of the LLM service layer within the Marka AI framework.

## Overview

The LLM layer is designed to be **provider-agnostic** while leveraging the **Google Agent Development Kit (ADK)** for advanced agentic orchestration. It uses **LiteLLM** as a bridge to support various model providers (Gemini, Mistral, Groq, etc.) through a unified interface.

## Key Components

### 1. `AgentRole` Enum (`ai/app/models/enums.py`)
To eliminate magic strings and ensure type safety, we use the `AgentRole` enum. 
- `ORCHESTRATOR`: Used for smart routing and tool selection.
- `CONTENT`: Optimized for Egyptian Arabic marketing copy generation.
- `RAG`: Handles brand context and product retrieval.
- `CHATBOT`: Manages general conversation and intent parsing.
- `EMBEDDING`: Generates vector embeddings for semantic search.

### 2. `LLMService` (`ai/app/services/llm_service.py`)
The central service that provides initialized ADK model instances to agents.
- **Model Resolution:** Maps `AgentRole` to specific model strings defined in `config.py`.
- **Environment Management:** Automatically injects `GEMINI_API_KEY` and `GOOGLE_API_KEY` into `os.environ` to satisfy ADK/LiteLLM requirements.
- **ADK Bridge:** Returns `google.adk.models.lite_llm.LiteLlm` objects, which are natively compatible with ADK Agents.

### 3. `Settings` (`ai/app/config.py`)
Uses `pydantic-settings` to load configuration from the root `.env` file.
- Ensures all model names and API keys are validated on startup.
- Centralizes model naming conventions (e.g., `gemini/` prefix and `-preview` suffix).

## Model Naming Conventions

For Google AI Studio (using an API key), we follow these rules:
1. **Prefix:** Must use `gemini/` (e.g., `gemini/gemini-3-flash-preview`). Using `google/` will attempt to route via Vertex AI.
2. **Suffix:** Currently, Gemini 3 models require the `-preview` suffix.

## Usage Example

```python
from google.adk import Agent
from app.services.llm_service import LLMService
from app.models.enums import AgentRole

# 1. Initialize service
llm_service = LLMService()

# 2. Get the configured ADK model for a role
model = llm_service.get_adk_model(AgentRole.ORCHESTRATOR)

# 3. Create an agent
agent = Agent(
    name="Orchestrator",
    model=model,
    instruction="You are the smart orchestrator..."
)
```

## Testing

- **Unit Tests:** Located in `ai/tests/unit/`, focusing on configuration and enum mapping.
- **Integration Tests:** Located in `ai/tests/integration/`, verifying real ADK model initialization and live API connectivity.
