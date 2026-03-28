from enum import Enum

class AgentRole(str, Enum):
    """Enumeration of agent roles within the AI system.

    Defines the specific functional domains and responsibilities assigned to different
    agents in the marketing automation framework.
    """
    
    ORCHESTRATOR = "orchestrator"
    """The central manager that coordinates tasks and delegates to specialized agents."""
    
    CONTENT = "content"
    """Agent specialized in generating marketing content (copy, posts, emails)."""
    
    RAG = "rag"
    """Agent specialized in Retrieval-Augmented Generation for knowledge base queries."""
    
    CHATBOT = "chatbot"
    """Agent focused on real-time customer interaction and support."""
    
    EMBEDDING = "embedding"
    """Agent specialized in vector embeddings for semantic search."""
