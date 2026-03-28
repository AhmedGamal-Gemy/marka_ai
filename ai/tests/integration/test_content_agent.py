# ai/tests/integration/test_content_agent.py
import pytest

from app.agents.content.agent import ContentAgent
from app.models.enums import EmailStrategy
from app.schemas.content import ContentResponse, MarketingEmail


@pytest.mark.asyncio
async def test_content_agent_generate_email(settings):
    """Verify ContentAgent generates a marketing email for a product.

    Arrange: Initialize ContentAgent with settings and a product description.
    Act: Call generate_email with a promotional strategy.
    Assert: Returns ContentResponse with thought_process and at least one email.
    """
    agent = ContentAgent(settings=settings)

    result = await agent.generate_email(
        product_description="ساعة ذكية جديدة بتصميم أنيق وبطارية تطول",
        strategy=EmailStrategy.PROMOTIONAL,
    )

    assert isinstance(result, ContentResponse)
    assert len(result.thought_process) > 0
    assert len(result.emails) >= 1

    email = result.emails[0]
    assert isinstance(email, MarketingEmail)
    assert len(email.subject) > 0
    assert email.strategy == EmailStrategy.PROMOTIONAL
    assert len(email.parts) >= 2


@pytest.mark.asyncio
async def test_content_agent_email_contains_arabic(settings):
    """Verify generated email content contains Arabic characters.

    Arrange: Initialize ContentAgent with a product.
    Act: Generate an email.
    Assert: Subject and at least one part contain Arabic text.
    """
    agent = ContentAgent(settings=settings)

    result = await agent.generate_email(
        product_description="منتج تجريبي للاختبار",
        strategy=EmailStrategy.NEWSLETTER,
    )

    email = result.emails[0]

    # Subject should contain Arabic
    has_arabic_subject = any("\u0600" <= char <= "\u06ff" for char in email.subject)
    assert has_arabic_subject, "Email subject should contain Arabic text"

    # At least one part should contain Arabic
    has_arabic_part = any(
        any("\u0600" <= char <= "\u06ff" for char in part.content)
        for part in email.parts
    )
    assert has_arabic_part, "Email parts should contain Arabic text"
