from enum import Enum

class AgentRole(str, Enum):
    ORCHESTRATOR = "orchestrator"
    CONTENT = "content"
    RAG = "rag"
    CHATBOT = "chatbot"
    EMBEDDING = "embedding"
