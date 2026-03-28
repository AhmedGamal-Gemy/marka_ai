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
