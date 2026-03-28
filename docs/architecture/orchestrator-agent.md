# Orchestrator Agent

The Orchestrator Agent is the primary routing "brain" of the Marka AI framework. It sits at the entry point of the AI layer and directs user messages to the appropriate specialized sub-agent.

## Key Features

### 1. Hybrid Chain-of-Thought (CoT)
The Orchestrator uses a structured Pydantic schema (`OrchestratorResponse`) that requires the model to generate a `thought_process` field (in English) before selecting the final `intent`. This ensures the model considers nuances in Egyptian Arabic and the conversation context before making a routing decision.

### 2. Google ADK Native
Built using the official Google Agent Development Kit, the Orchestrator leverages the `Agent` and `Runner` patterns for session management and tool-ready execution.

### 3. Intent Mapping
Currently, the Orchestrator supports the following routing intents:
- `CHATBOT`: Greetings and general assistance.
- `CONTENT`: Marketing content generation requests.
- `RAG`: Brand and product-specific queries.

## Usage

```python
from app.agents.orchestrator import OrchestratorAgent

orchestrator = OrchestratorAgent()
result = await orchestrator.parse_intent("عايز أعمل بوست جديد")

print(f"Reasoning: {result.thought_process}")
print(f"Route to: {result.intent}")
```

## Testing

Integration tests verify the routing logic with live prompts from the Gemini 3 Flash model.
- `ai/tests/integration/test_orchestrator_agent.py`
