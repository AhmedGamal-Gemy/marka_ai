import pytest
from pydantic import ValidationError

from app.models.enums import EmailStrategy
from app.schemas.content import (
    ContentResponse,
    EmailPart,
    EmailRecipient,
    EmailSender,
    MarketingEmail,
)


# ---------------------------------------------------------------------------
# EmailPart tests
# ---------------------------------------------------------------------------


def test_email_part_valid():
    """Verify EmailPart parses correctly with role and content.

    Arrange: Create a dict with role and content.
    Act: Instantiate EmailPart.
    Assert: Fields are populated correctly.
    """
    part = EmailPart(role="header", content="أهلاً بيك في عرضنا الجديد!")
    assert part.role == "header"
    assert part.content == "أهلاً بيك في عرضنا الجديد!"


def test_email_part_missing_content():
    """Verify EmailPart raises ValidationError when content is missing.

    Arrange: Create a dict with only role.
    Act & Assert: ValidationError is raised.
    """
    with pytest.raises(ValidationError):
        EmailPart(role="body")


# ---------------------------------------------------------------------------
# EmailStrategy enum tests
# ---------------------------------------------------------------------------


def test_email_strategy_values():
    """Verify all expected strategy types exist.

    Arrange & Act: Check enum members.
    Assert: All 7 strategy types are present.
    """
    expected = {
        "promotional",
        "newsletter",
        "welcome",
        "abandoned_cart",
        "re_engagement",
        "product_launch",
        "seasonal",
    }
    assert {s.value for s in EmailStrategy} == expected


def test_email_strategy_from_string():
    """Verify EmailStrategy can be created from string value.

    Arrange: A valid strategy string.
    Act: Create enum from string.
    Assert: Matches the correct enum member.
    """
    assert EmailStrategy("promotional") == EmailStrategy.PROMOTIONAL
    assert EmailStrategy("seasonal") == EmailStrategy.SEASONAL


# ---------------------------------------------------------------------------
# MarketingEmail tests
# ---------------------------------------------------------------------------


def _make_valid_email() -> dict:
    """Helper to build a valid MarketingEmail dict."""
    return {
        "subject": "عرض خاص بس ليوم!",
        "strategy": "promotional",
        "parts": [
            {"role": "header", "content": "أهلاً بيك!"},
            {"role": "body", "content": "عندنا عرض خاص على كل المنتجات."},
            {"role": "call_to_action", "content": "اطلب دلوقتي!"},
        ],
    }


def test_marketing_email_valid():
    """Verify a complete MarketingEmail parses correctly.

    Arrange: A valid email dict with subject, strategy, and parts.
    Act: Instantiate MarketingEmail.
    Assert: All fields populated, parts list has 3 items.
    """
    email = MarketingEmail(**_make_valid_email())
    assert email.subject == "عرض خاص بس ليوم!"
    assert email.strategy == EmailStrategy.PROMOTIONAL
    assert len(email.parts) == 3
    assert email.parts[0].role == "header"
    assert email.to is None
    assert email.sender is None


def test_marketing_email_with_recipient_and_sender():
    """Verify optional to and sender fields parse correctly.

    Arrange: Email dict with recipient and sender added.
    Act: Instantiate MarketingEmail.
    Assert: to and sender are populated with correct types.
    """
    data = _make_valid_email()
    data["to"] = {"name": "أحمد", "email": "ahmed@example.com"}
    data["sender"] = {"name": "ماركاي", "email": "hello@marka.ai"}

    email = MarketingEmail(**data)
    assert isinstance(email.to, EmailRecipient)
    assert email.to.name == "أحمد"
    assert isinstance(email.sender, EmailSender)
    assert email.sender.name == "ماركاي"


def test_marketing_email_optional_fields_default_none():
    """Verify to and sender default to None when omitted.

    Arrange: Email dict without to/sender.
    Act: Instantiate MarketingEmail.
    Assert: to and sender are None.
    """
    email = MarketingEmail(**_make_valid_email())
    assert email.to is None
    assert email.sender is None


def test_marketing_email_invalid_strategy():
    """Verify invalid strategy string raises ValidationError.

    Arrange: Email dict with an unknown strategy value.
    Act & Assert: ValidationError is raised.
    """
    data = _make_valid_email()
    data["strategy"] = "unknown_strategy"
    with pytest.raises(ValidationError):
        MarketingEmail(**data)


def test_marketing_email_missing_subject():
    """Verify missing subject raises ValidationError.

    Arrange: Email dict without subject.
    Act & Assert: ValidationError is raised.
    """
    data = _make_valid_email()
    del data["subject"]
    with pytest.raises(ValidationError):
        MarketingEmail(**data)


# ---------------------------------------------------------------------------
# ContentResponse tests
# ---------------------------------------------------------------------------


def _make_valid_response() -> dict:
    """Helper to build a valid ContentResponse dict."""
    return {
        "thought_process": "User wants a promotional email for a new watch.",
        "emails": [_make_valid_email()],
    }


def test_content_response_valid():
    """Verify ContentResponse parses with thought_process and emails list.

    Arrange: A valid response dict with one email.
    Act: Instantiate ContentResponse.
    Assert: thought_process and emails are populated.
    """
    response = ContentResponse(**_make_valid_response())
    assert len(response.thought_process) > 0
    assert len(response.emails) == 1
    assert isinstance(response.emails[0], MarketingEmail)


def test_content_response_multiple_emails():
    """Verify ContentResponse accepts multiple email options.

    Arrange: Response with 3 different emails.
    Act: Instantiate ContentResponse.
    Assert: All 3 emails are present.
    """
    data = _make_valid_response()
    data["emails"] = [_make_valid_email() for _ in range(3)]
    response = ContentResponse(**data)
    assert len(response.emails) == 3


def test_content_response_missing_emails():
    """Verify missing emails field raises ValidationError.

    Arrange: Response dict without emails.
    Act & Assert: ValidationError is raised.
    """
    with pytest.raises(ValidationError):
        ContentResponse(thought_process="some reasoning")


def test_content_response_empty_emails():
    """Verify ContentResponse accepts empty emails list.

    Arrange: Response with empty emails list.
    Act: Instantiate ContentResponse.
    Assert: emails is an empty list.
    """
    response = ContentResponse(thought_process="No emails.", emails=[])
    assert response.emails == []
