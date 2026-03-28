# Orchestrator Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the primary routing brain of Marka AI that parses user intent and directs traffic to specialized sub-agents using a hybrid CoT + Structured Output pattern.

**Architecture:**
- **Schema:** A Pydantic model (`OrchestratorResponse`) that forces a `thought_process` field before the `intent`.
- **Agent:** A Google ADK `LlmAgent` configured with the `gemini-3-flash-preview` model and strict JSON output.
- **Routing:** A service-level method that invokes the agent and returns the parsed intent.

**Tech Stack:** Python 3.12, Google ADK, Pydantic, pytest

---

### Task 1: Create Orchestrator Response Schema

**Files:**
- Create: `ai/app/schemas/orchestrator.py`
- Create: `ai/tests/unit/test_orchestrator_schema.py`

- [ ] **Step 1: Write the failing test**

```python
# ai/tests/unit/test_orchestrator_schema.py
import pytest
from pydantic import ValidationError
from app.schemas.orchestrator import OrchestratorResponse
from app.models.enums import AgentRole

def test_orchestrator_response_valid():
    """Verify valid JSON parsing."""
    data = {
        "thought_process": "User said hi.",
        "intent": "chatbot"
    }
    response = OrchestratorResponse(**data)
    assert response.intent == AgentRole.CHATBOT

def test_orchestrator_response_invalid_role():
    """Verify validation fails for unknown roles."""
    with pytest.raises(ValidationError):
        OrchestratorResponse(thought_process="...", intent="unknown_role")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ai && uv run pytest tests/unit/test_orchestrator_schema.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.schemas.orchestrator'`

- [ ] **Step 3: Implement the schema**

```python
# ai/app/schemas/orchestrator.py
from pydantic import BaseModel, Field
from app.models.enums import AgentRole

class OrchestratorResponse(BaseModel):
    """
    Structured response from the Orchestrator.
    Field order is critical: 'thought_process' first forces Chain-of-Thought.
    """
    thought_process: str = Field(
        description="Step-by-step reasoning in English to determine the user's intent, considering Egyptian Arabic nuances."
    )
    intent: AgentRole = Field(
        description="The final selected role for the next turn."
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ai && uv run pytest tests/unit/test_orchestrator_schema.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ai/app/schemas/orchestrator.py ai/tests/unit/test_orchestrator_schema.py
git commit -m "feat(ai): add OrchestratorResponse schema with CoT field"
```

### Task 2: Implement the Orchestrator Agent logic

**Files:**
- Create: `ai/app/agents/orchestrator.py`
- Create: `ai/tests/integration/test_orchestrator_agent.py`

- [ ] **Step 1: Write the integration test (Mocked LLM if possible, or live)**

We'll use a live test to ensure the CoT actually works with Gemini 3 Flash.

```python
# ai/tests/integration/test_orchestrator_agent.py
import pytest
import os
from app.agents.orchestrator import OrchestratorAgent
from app.models.enums import AgentRole

@pytest.mark.asyncio
async def test_orchestrator_routing_logic():
    # Ensure test key is present in environment
    # os.environ["LLM_API_KEY"] = "your-key-here"
    
    agent = OrchestratorAgent()
    
    # Test case: Content generation intent
    result = await agent.parse_intent("عايز أعمل بوست للساعة الجديدة")
    assert result.intent == AgentRole.CONTENT
    assert len(result.thought_process) > 0
    
    # Test case: Greeting intent
    result = await agent.parse_intent("أهلا")
    assert result.intent == AgentRole.CHATBOT
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ai && uv run pytest tests/integration/test_orchestrator_agent.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.agents.orchestrator'`

- [ ] **Step 3: Implement the OrchestratorAgent class**

```python
# ai/app/agents/orchestrator.py
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from app.services.llm_service import LLMService
from app.models.enums import AgentRole
from app.schemas.orchestrator import OrchestratorResponse

class OrchestratorAgent:
    """
    The primary routing agent for Marka AI.
    Uses Gemini 3 Flash to parse intent via structured CoT.
    """
    def __init__(self):
        self.llm_service = LLMService()
        self.session_service = InMemorySessionService()
        
        # Configure the ADK Agent
        self.agent = Agent(
            name="Orchestrator",
            model=self.llm_service.get_adk_model(AgentRole.ORCHESTRATOR),
            instruction=(
                "You are the Marka AI Orchestrator. Your job is to route user messages to the correct sub-agent.\n"
                "Analyze the user's message in English in the 'thought_process' field first.\n"
                "Then, pick the correct 'intent' from the AgentRole list.\n"
                "Available intents:\n"
                "- 'chatbot': Greetings, help, or casual chat.\n"
                "- 'content': Requests to create posts, captions, or marketing content.\n"
                "- 'rag': Specific questions about products or brand information.\n"
                "If ambiguous, default to 'chatbot' and ask for more details."
            ),
            # Force structured output using our schema
            response_schema=OrchestratorResponse
        )

    async def parse_intent(self, user_text: str) -> OrchestratorResponse:
        """Invokes the agent and returns the structured response."""
        async with Runner(
            app_name="MarkaAI",
            agent=self.agent,
            session_service=self.session_service,
            auto_create_session=True
        ) as runner:
            
            message = types.Content(
                role="user", 
                parts=[types.Part.from_text(text=user_text)]
            )
            
            # We take the first complete response from the generator
            async for event in runner.run_async(
                user_id="internal_tester",
                session_id="orchestrator_parse",
                new_message=message
            ):
                # ADK with response_schema populates event.content
                if hasattr(event, 'content') and event.content:
                    # In ADK, structured output is often parsed into event.content
                    # This depends on the exact version/plugin behavior
                    # We'll adapt based on the actual event structure
                    return event.content
            
            raise ValueError("No response generated by Orchestrator")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ai && uv run pytest tests/integration/test_orchestrator_agent.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ai/app/agents/orchestrator.py ai/tests/integration/test_orchestrator_agent.py
git commit -m "feat(ai): implement OrchestratorAgent with ADK and structured output"
```
