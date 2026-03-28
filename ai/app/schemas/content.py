from pydantic import BaseModel, Field

from app.models.enums import EmailStrategy


class EmailPart(BaseModel):
    """A single section of a marketing email.

    Emails are composed of ordered parts (e.g., header, body, CTA).
    Each part has a role and content in Egyptian Arabic dialect.
    """

    role: str = Field(
        description=(
            "The role of this part in the email structure. "
            "Examples: 'header', 'body', 'call_to_action', 'footer', 'ps'."
        )
    )
    content: str = Field(
        description=(
            "The text content for this email part, written in Egyptian Arabic dialect."
        )
    )


class EmailRecipient(BaseModel):
    """Optional recipient details for personalization."""

    name: str | None = Field(
        default=None,
        description="Recipient display name for personalization.",
    )
    email: str | None = Field(
        default=None,
        description="Recipient email address.",
    )


class EmailSender(BaseModel):
    """Optional sender details for the From field."""

    name: str | None = Field(
        default=None,
        description="Sender display name (e.g., brand name).",
    )
    email: str | None = Field(
        default=None,
        description="Sender email address.",
    )


class MarketingEmail(BaseModel):
    """A complete marketing email ready to be sent.

    Contains the subject line, ordered body parts, strategy type,
    and optional sender/recipient personalization fields.
    """

    subject: str = Field(
        description=(
            "Email subject line in Egyptian Arabic. Should be catchy, "
            "concise, and encourage the recipient to open the email."
        )
    )
    strategy: EmailStrategy = Field(
        description=(
            "The marketing strategy type for this email. "
            "Determines the tone and structure of the content."
        )
    )
    parts: list[EmailPart] = Field(
        description=(
            "Ordered list of email sections. Typically includes at least "
            "'header', 'body', and 'call_to_action' parts."
        )
    )
    to: EmailRecipient | None = Field(
        default=None,
        description="Optional recipient details for personalization.",
    )
    sender: EmailSender | None = Field(
        default=None,
        description="Optional sender details for the From field.",
    )


class ContentResponse(BaseModel):
    """Structured response schema for the Content Agent.

    Enforces Chain-of-Thought (CoT) reasoning before generating
    marketing email options in Egyptian Arabic dialect.
    """

    thought_process: str = Field(
        description=(
            "Step-by-step reasoning in English. MUST be generated first "
            "to analyze the product, target audience, and email strategy "
            "before crafting the emails."
        )
    )
    emails: list[MarketingEmail] = Field(
        description=(
            "Generated marketing email options. Each email includes a "
            "subject line, strategy type, ordered body parts, and "
            "optional sender/recipient fields."
        )
    )
