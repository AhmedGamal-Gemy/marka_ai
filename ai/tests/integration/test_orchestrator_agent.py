# ai/tests/integration/test_orchestrator_agent.py
import pytest
import os
from app.agents.orchestrator.agent import OrchestratorAgent
from app.models.enums import AgentRole

@pytest.mark.asyncio
async def test_orchestrator_routing_logic(settings):
    # API Key is pulled automatically from settings fixture
    agent = OrchestratorAgent(settings=settings)
    
    # Test case: Content generation intent
    result = await agent.parse_intent("عايز أعمل بوست للساعة الجديدة")
    assert result.intent == AgentRole.CONTENT
    assert len(result.thought_process) > 0
    
    # Test case: Greeting intent
    result = await agent.parse_intent("أهلا")
    assert result.intent == AgentRole.CHATBOT
