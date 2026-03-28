<!-- Context: project-intelligence/technical | Priority: high | Version: 1.0 | Updated: 2026-03-29 -->

# Technical Domain — Marka AI

> Technical foundation, architecture, and key patterns for the Marka AI marketing automation platform.

## Quick Reference

- **Purpose**: Understand how the project works technically
- **Update When**: New features, refactoring, tech stack changes
- **Audience**: Developers, DevOps, technical stakeholders

## Primary Stack

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Language | Python | 3.12+ | ADK compatibility, async support |
| Framework | FastAPI | Latest | Async, OpenAPI, Pydantic integration |
| AI SDK | Google ADK | 1.28+ | Native Gemini support, structured output |
| LLM | Google Gemini | 3.x | Arabic dialect support, structured output |
| Database | MongoDB | 8.0 | Flexible document store for job state |
| Vector DB | Qdrant | 1.17 | 768-dim embeddings, semantic search |
| Package Mgr | uv | Latest | Fast, lockfile-based Python deps |
| Linting | ruff | Latest | Fast, replaces flake8+black+isort |
| Type Check | mypy | Latest | Static type verification |

## Architecture Pattern

```
Type: Agent-based (two-layer)
Pattern: Smart Orchestrator → Specialized Agents
Layers: AI Layer (FastAPI + Agents) + Frontend Layer (Bot + Web)
```

## Project Structure

```
ai/app/
├── agents/           # ADK agents (orchestrator, content, rag, chatbot)
│   ├── orchestrator/ # Intent routing agent
│   └── content/      # Marketing email generation
├── api/v1/           # FastAPI route handlers
├── middleware/        # Auth (X-API-Token), rate limiting
├── models/           # Enums (AgentRole, EmailStrategy)
├── schemas/          # Pydantic request/response models
├── services/         # LLMService, QdrantService, MongoDBService
├── tools/            # ADK FunctionTools
├── config.py         # pydantic-settings Settings class
└── main.py           # FastAPI app entry point
```

## Agent Pattern (Established)

Every agent follows this pattern:

```python
class SomeAgent:
    def __init__(self, settings=None):
        self.llm_service = LLMService(settings=settings)
        self.session_service = InMemorySessionService()
        self.agent = Agent(
            name="AgentName",
            model=self.llm_service.get_adk_model(AgentRole.ROLE),
            instruction="...",
            output_schema=ResponseSchema
        )

    async def method(self, input: str) -> ResponseSchema:
        async with Runner(app_name="MarkaAI", agent=self.agent,
                         session_service=self.session_service,
                         auto_create_session=True) as runner:
            message = types.Content(role="user",
                                   parts=[types.Part.from_text(text=input)])
            async for event in runner.run_async(...):
                if hasattr(event, 'content') and event.content.parts:
                    raw_text = event.content.parts[0].text
                    if raw_text:
                        return ResponseSchema.model_validate_json(raw_text)
            raise ValueError("No response generated")
```

**Key rules:**
- `LLMService` sets `GEMINI_API_KEY` env var (ADK reads from env, not constructor)
- `output_schema` on Agent for structured JSON output
- `model_validate_json()` to parse response
- Settings dependency injection via constructor
- Google-style docstrings on all public methods

## Email Schema Pattern

```
ContentResponse
├── thought_process: str              # CoT reasoning in English
└── emails: list[MarketingEmail]
    ├── subject: str                  # Egyptian Arabic subject
    ├── strategy: EmailStrategy       # Enum: 7 campaign types
    ├── parts: list[EmailPart]        # Ordered sections
    │   ├── role: str                 # header, body, call_to_action, footer, ps
    │   └── content: str              # Egyptian Arabic text
    ├── to: EmailRecipient | None     # Optional personalization
    └── sender: EmailSender | None    # Optional From field
```

## LLM Strategy

| Role | Model | Purpose |
|------|-------|---------|
| Orchestrator | `gemini/gemini-3-flash-preview` | Intent routing |
| Content | `gemini/gemini-3.1-pro-preview` | Egyptian Arabic copy |
| RAG / Chatbot | `gemini/gemini-3.1-flash-lite-preview` | Fast workers |
| Embedding | `gemini/gemini-embedding-2` | Vector embeddings |

## Key Conventions

- **Auth:** `X-API-Token` header (not `Authorization: Bearer`)
- **LLM prefix:** `gemini/` prefix for Google AI Studio models
- **Embeddings:** 768 dimensions — must match Qdrant config
- **Imports:** Absolute only (`from app.xxx import yyy`)
- **Types:** Modern union (`str | None`), complete hints on all public signatures
- **Commits:** Conventional (`feat(ai):`, `fix(bot):`, `docs:`, `chore:`)
- **Git identity:** Use `gh api user`, never hardcode config

## Onboarding Checklist

- [ ] Know the primary tech stack and versions
- [ ] Understand the agent pattern (LLMService → Agent → Runner)
- [ ] Know the email schema structure
- [ ] Understand the LLM strategy (which model for which role)
- [ ] Be able to run tests: `cd ai && uv run pytest`
- [ ] Know the git identity rule (use `gh api user`)

## Related Files

- `living-notes.md` — Current status, open questions
- `decisions-log.md` — Decision history
- `MARKA_AI_Technical_Document.md` — Full architecture spec
- `AGENTS.md` — AI agent instructions
