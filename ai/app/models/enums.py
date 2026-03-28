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


class EmailStrategy(str, Enum):
    """Marketing email strategy types.

    Defines the purpose and tone of a marketing email campaign,
    guiding the Content Agent in generating appropriate copy.
    """

    PROMOTIONAL = "promotional"
    """Sales, discounts, limited-time offers."""

    NEWSLETTER = "newsletter"
    """Regular updates, tips, industry news."""

    WELCOME = "welcome"
    """Onboarding new subscribers or customers."""

    ABANDONED_CART = "abandoned_cart"
    """Recover users who left items in their cart."""

    RE_ENGAGEMENT = "re_engagement"
    """Win back inactive subscribers."""

    PRODUCT_LAUNCH = "product_launch"
    """Announce a new product or feature."""

    SEASONAL = "seasonal"
    """Holiday or event-based campaigns (Ramadan, Eid, etc.)."""
