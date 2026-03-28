from pydantic import BaseModel, Field


class ContentResponse(BaseModel):
    """
    Structured response schema for the Content agent.

    This schema enforces a Chain-of-Thought (CoT) pattern by requiring the
    'thought_process' field to be generated before the final 'captions'.
    The agent reasons about the product in English, then produces marketing
    captions in Egyptian Arabic dialect for SME audiences.
    """

    thought_process: str = Field(
        description=(
            "A step-by-step reasoning string in English. This field MUST be "
            "generated first to ensure the LLM correctly analyzes the product "
            "description and target audience before crafting captions."
        )
    )
    captions: list[str] = Field(
        description=(
            "Exactly 3 marketing captions written in Egyptian Arabic dialect. "
            "Each caption should be engaging, concise, and suitable for social "
            "media marketing targeting small and medium enterprises (SMEs)."
        )
    )
