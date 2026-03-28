# AGENTS.md — Marka AI

Instructions for AI coding agents working in this repository.

## Build & Run

This project uses `uv` for Python dependency management. Never use `pip` directly.

```bash
# Install dependencies (creates .venv automatically)
uv sync

# Add a dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Run the FastAPI dev server
uv run fastapi dev ai/app/main.py

# Run Docker stack (MongoDB, Qdrant, FastAPI, Bot, Web)
docker compose up --build
```

## Testing

```bash
# Run all tests (from ai/ directory)
cd ai && uv run pytest

# Run a single test file
uv run pytest tests/unit/test_config.py

# Run a single test by name
uv run pytest -k "test_settings_loads_env_vars"

# Run with verbose output
uv run pytest -v

# Run only unit or integration tests
uv run pytest tests/unit/
uv run pytest tests/integration/
```

Test config: `ai/pyproject.toml` sets `pythonpath = "."` so imports like `from app.config import ...` work. Tests live in `ai/tests/unit/` and `ai/tests/integration/`. Async tests use `@pytest.mark.asyncio`.

## Linting & Formatting

```bash
# Lint and auto-fix
uv run ruff check --fix .

# Format code
uv run ruff format .

# Type check
uv run mypy ai/app/
```

Ruff config lives in root `pyproject.toml`. Target: Python 3.12+, 120-char lines.

## Code Style

### Imports
- **Absolute imports only** — never use relative (`from ..utils import x`)
- Group order: stdlib → third-party → local, separated by blank lines
```python
import os
from pathlib import Path

from pydantic import BaseModel
from fastapi import FastAPI

from app.config import get_settings
from app.models.enums import AgentRole
```

### Naming
- `snake_case` for functions, variables, modules
- `PascalCase` for classes
- `SCREAMING_SNAKE_CASE` for module-level constants
- Acronyms stay uppercase: `HTTPClient`, `LLMService`

### Types
- **All public function signatures must have complete type hints** — parameters and return types
- Use modern union syntax: `str | None` not `Optional[str]`
- Use `list[str]` not bare `list`
- Pydantic models for all request/response boundaries

### Docstrings
- Google-style docstrings required on all public classes, methods, and functions
```python
def get_model_for_role(self, role: AgentRole) -> str:
    """Retrieves the assigned model for a specific agent role.

    Args:
        role: The functional role of the agent.

    Returns:
        The model identifier string for the given role.

    Raises:
        ValueError: If the provided role is not recognized.
    """
```

### Error Handling
- Use specific exceptions (`ValueError`, `TypeError`, `RuntimeError`) — never bare `except Exception:`
- Pydantic for input validation at API/agent boundaries
- Chain exceptions with `raise ... from e` to preserve context
- Custom exceptions should carry structured info (status codes, retry hints)

### Async
- Use `async def` for all FastAPI endpoints and agent operations
- Google ADK agents require the `Runner` + `SessionService` pattern (not `.run()`)
- Use `pytest-asyncio` with `@pytest.mark.asyncio` for async tests

## Project Structure

```
ai/app/
├── agents/       # Orchestrator, RAG, Content, Chatbot agents
├── api/v1/       # FastAPI route handlers
├── middleware/    # Auth (X-API-Token), rate limiting
├── models/       # Enums, Pydantic models
├── schemas/      # Request/response schemas
├── services/     # LLMService, QdrantService, MongoDBService
├── config.py     # pydantic-settings Settings class
└── main.py       # FastAPI app entry point
```

## Key Conventions

- **Auth:** Use `X-API-Token` header (not `Authorization: Bearer`) for inter-component auth
- **LLM prefix:** Google models use `gemini/` prefix (e.g., `gemini/gemini-3-flash-preview`)
- **Embeddings:** 768 dimensions — must match Qdrant config
- **State:** In-memory job state is acceptable for v1; durable logs go to MongoDB
- **Commits:** Conventional commits: `feat(ai):`, `fix(bot):`, `docs:`, `chore:`
- **Branches:** `feature/ai/*`, `feature/bot/*`, `feature/web/*` → merge to `develop`
- **PRs:** Require 1 approval, lint + tests must pass, no debug prints

## Git Identity

**NEVER hardcode `git config user.name` / `git config user.email`.** This repo has no local git identity by design. Always use the GitHub CLI to get the authenticated user:

```bash
# Get GitHub username
gh api user --jq '.login'

# Commit with correct author (use noreply email)
git commit --author="$(gh api user --jq '.login') <$(gh api user --jq '.login')@users.noreply.github.com>" -m "feat(ai): description"
```

## Architecture

Two-layer system: **AI Layer** (FastAPI + agents) and **Frontend Layer** (Telegram Bot + React).

Smart Orchestrator LLM strategy:
| Role | Model | Purpose |
|------|-------|---------|
| Orchestrator | `gemini/gemini-3-flash-preview` | Intent routing |
| Content | `gemini/gemini-3.1-pro-preview` | Egyptian Arabic copy |
| RAG / Chatbot | `gemini/gemini-3.1-flash-lite-preview` | Fast workers |
| Embedding | `gemini/gemini-embedding-2` | Vector embeddings |

See `MARKA_AI_Technical_Document.md` for full architecture details.
