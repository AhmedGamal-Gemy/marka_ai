from pydantic import BaseModel, Field
from app.models.enums import AgentRole

class OrchestratorResponse(BaseModel):
    """
    Structured response schema for the Orchestrator agent.
    
    This schema enforces a Chain-of-Thought (CoT) pattern by requiring the
    'thought_process' field to be generated before the final 'intent'.
    The reasoning should prioritize understanding user needs in both
    Standard Arabic and Egyptian colloquialisms.
    """
    thought_process: str = Field(
        description=(
            "A step-by-step reasoning string in English. This field MUST be "
            "generated first to ensure the LLM correctly evaluates the user's "
            "request before selecting a routing intent."
        )
    )
    intent: AgentRole = Field(
        description=(
            "The final classified intent/role for the next interaction turn. "
            "Valid roles are defined in the AgentRole enum (e.g., 'chatbot', 'content', 'rag')."
        )
    )
