import asyncio
import os
import pytest
from app.services.llm_service import LLMService
from app.models.enums import AgentRole
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

@pytest.mark.asyncio
async def test_agent(settings):
    print("--- 1. Testing Environment ---")
    # API Key is pulled automatically from settings fixture
    
    print("--- 2. Initializing LLM Service ---")
    service = LLMService(settings=settings)
    
    print("--- 3. Fetching Orchestrator Model ---")
    model = service.get_adk_model(AgentRole.ORCHESTRATOR)
    print(f"Model configured as: {model.model}")
    
    print("--- 4. Building ADK Agent ---")
    agent = Agent(
        name="TestAgent",
        model=model,
        instruction="You are a helpful assistant. Reply with exactly the phrase: HELLO FROM GOOGLE ADK"
    )
    
    print("--- 5. Running Agent via Runner ---")
    try:
        session_service = InMemorySessionService()
        
        async with Runner(
            app_name="TestApp",
            agent=agent, 
            session_service=session_service,
            auto_create_session=True 
        ) as runner:
            
            print("--- FINAL RESPONSE ---")
            
            message = types.Content(role="user", parts=[types.Part.from_text(text="Say hello!")])
            
            async for event in runner.run_async(
                user_id="user_1",
                session_id="test_session_1",
                new_message=message
            ):
                print(f"DEBUG: Event received: {type(event).__name__}")
                if hasattr(event, 'text') and event.text:
                    print(f"TEXT: {event.text}")
                else:
                    print(f"RAW: {event}")
            print("\n----------------------")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    print("Starting async test...")
    asyncio.run(test_agent())
