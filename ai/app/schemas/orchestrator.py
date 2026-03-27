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
