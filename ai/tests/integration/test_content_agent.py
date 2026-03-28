# ai/tests/integration/test_content_agent.py
import pytest
from app.agents.content.agent import ContentAgent
from app.schemas.content import ContentResponse


@pytest.mark.asyncio
async def test_content_agent_generate_captions(settings):
    """Verify ContentAgent generates 3 Egyptian Arabic captions for a product.

    Arrange: Initialize ContentAgent with settings fixture and a product description.
    Act: Call generate_captions with an Egyptian Arabic product description.
    Assert: Returns ContentResponse with non-empty thought_process and 3 captions.
    """
    agent = ContentAgent(settings=settings)

    result = await agent.generate_captions("ساعة ذكية جديدة بتصميم أنيق وبطارية تطول")

    assert isinstance(result, ContentResponse)
    assert len(result.thought_process) > 0
    assert len(result.captions) == 3
    assert all(isinstance(c, str) for c in result.captions)
    assert all(len(c) > 0 for c in result.captions)


@pytest.mark.asyncio
async def test_content_agent_captions_are_egyptian_arabic(settings):
    """Verify generated captions contain Arabic characters.

    Arrange: Initialize ContentAgent with a simple product.
    Act: Generate captions.
    Assert: At least one caption contains Arabic Unicode characters.
    """
    agent = ContentAgent(settings=settings)

    result = await agent.generate_captions("منتج تجريبي للاختبار")

    # Check at least one caption contains Arabic characters (Unicode range)
    has_arabic = any(
        any("\u0600" <= char <= "\u06ff" for char in caption)
        for caption in result.captions
    )
    assert has_arabic, "Captions should contain Arabic text"
