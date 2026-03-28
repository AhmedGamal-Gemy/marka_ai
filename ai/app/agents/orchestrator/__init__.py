from .agent import OrchestratorAgent

# ADK Discovery requires a variable named 'root_agent'
orchestrator_instance = OrchestratorAgent()
root_agent = orchestrator_instance.agent
