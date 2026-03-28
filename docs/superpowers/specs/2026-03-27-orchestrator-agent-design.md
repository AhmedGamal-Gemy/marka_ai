# Orchestrator Agent Design Specification

**Status:** Draft
**Date:** 2026-03-27
**Owner:** Ahmed
**Goal:** Implement the primary routing brain of Marka AI that parses user intent and directs traffic to specialized sub-agents.

## 1. Architecture Overview

The Orchestrator acts as the entry point for all user messages. It uses a **Hybrid Chain-of-Thought (CoT) + Structured Output** pattern to maximize routing accuracy.

### 1.1 Decision Flow
1. User message arrives.
2. Orchestrator invokes LLM (Gemini 3 Flash) with a strict Pydantic schema.
3. LLM generates a step-by-step English reasoning (`thought_process`).
4. LLM selects a target `AgentRole` based on the reasoning.
5. Orchestrator hands off execution to the selected sub-agent (or handles it directly if a simple greeting).

## 2. Components

### 2.1 Pydantic Response Schema (`ai/app/schemas/orchestrator.py`)
```python
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

### 2.2 Intent Mapping
The Orchestrator maps user input to the following `AgentRole` values:
- `CHATBOT`: Casual greetings, help requests, or general chitchat.
- `CONTENT`: Explicit requests to generate social media posts, captions, or ads.
- `RAG`: Questions requiring brand knowledge or product-specific details.

## 3. Data Flow

1. **Input:** `UserMessage(text="عايز أعمل بوست للساعة الجديدة")`
2. **LLM Output (Internal):**
   ```json
   {
     "thought_process": "User is asking to 'do a post' (عايز أعمل بوست) for a 'new watch'. This is a clear request for content generation.",
     "intent": "content"
   }
   ```
3. **Action:** Orchestrator logs the `thought_process` to MongoDB and routes the request to the `ContentAgent`.

## 4. Error Handling
- **Invalid Schema:** If the LLM fails to output valid JSON, the Orchestrator defaults to `CHATBOT` and requests clarification.
- **Ambiguous Input:** The prompt instructs the model to select `CHATBOT` and ask a clarifying question if the intent is not clear.

## 5. Testing Strategy
- **Unit Tests:** Verify that the `OrchestratorResponse` schema correctly validates and parses JSON.
- **Integration Tests:** Use real-world Egyptian Arabic prompts to verify that the LLM selects the correct `AgentRole`.
