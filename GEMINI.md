# Marka AI: Instructional Context

Welcome to the **Marka AI** project. This document serves as the primary instructional context for all AI interactions within this workspace, reflecting the "v1 Architecture & Technical Document".

## 🚀 Product Overview
Marka AI is an Autonomous AI Marketing Automation Framework focused on an Arabic-first experience for Egyptian SMEs. It automates marketing content creation, scheduling, and publishing without requiring marketing expertise, utilizing Egyptian Arabic dialect tuning.

### Key Characteristics
- **Audience:** Egyptian SMEs.
- **Goal:** Fully automated workflow from product description to published posts.
- **Language Focus:** Native Arabic-first generation.

## 🏗 System Architecture (v1)
The system is built as a Two-Layer Architecture:

1.  **AI Layer (FastAPI Backend):**
    *   **Core:** FastAPI, Pydantic, python-telegram-bot.
    *   **State & Memory:** MongoDB (Structured data: brand memories, job history).
    *   **RAG (Retrieval-Augmented Generation):** Qdrant (Vector embeddings for semantic search).
    *   **LLM Interface (Smart Strategy):** LiteLLM configured as:
        *   **Orchestrator:** `google/gemini-3-flash` (Smart tool caller)
        *   **Content Agent:** `google/gemini-3.1-pro` (Egyptian Arabic copy)
        *   **RAG/Chatbot:** `google/gemini-3.1-flash-lite` (Fast workers)
        *   **Embeddings:** `google/gemini-embedding-2`
    *   **Agents:** Orchestrator (routing), RAG Agent (brand context), Chatbot Agent (intent parsing), Content Agent (Arabic copy generation).
2.  **Frontend Layer:**
    *   Telegram Bot + React UI.

### Communication Flow
- **Frontend -> FastAPI:** Authenticated via `X-API-Token` header.
- **FastAPI -> LLMs:** Authenticated via API key, managed by LiteLLM.

## 🛠 Building and Running
The system relies heavily on Docker for deployment (FastAPI, MongoDB, Qdrant).
*(Detailed build/run commands are to be established based on the `docker-compose` setup as the project is initialized).*

**For Python Development (AI Layer):**
This project uses `uv` for fast Python dependency and environment management.

```bash
# 1. Install dependencies and create the virtual environment
uv sync

# 2. Add a new package
uv add <package_name>

# 3. Add a development dependency
uv add --dev <package_name>
```

**Note:** You do not need to manually activate the virtual environment if you prefix your commands with `uv run` (e.g., `uv run python main.py`).

## 🧪 Testing

Run tests using `pytest` via `uv`:

```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_chatbot.py

# Run tests matching a specific string
uv run pytest -k "test_intent"

# Run tests with verbose output
uv run pytest -v
```

## ⚡ PowerShell Productivity

Helpful commands for Windows development:

```powershell
# Set an environment variable for the current session
$env:OPENAI_API_KEY="your-key-here"

# Quickly search for a string across all Python files
Select-String -Pattern "class ChatbotAgent" -Path "*.py" -Recurse

# Stop a runaway Python process
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force
```

## 📏 Development Conventions
This project strictly enforces modern Python engineering standards. When writing or modifying code, agents MUST adhere to the guidance provided in `.agents/skills/`.

### 1. Code Style & Documentation (`python-code-style`)
- **Tooling:** Use `ruff` for linting and formatting (replaces flake8, isort, black).
- **Line Length:** 120 characters.
- **Naming:** Follow PEP 8 (snake_case for functions/variables, PascalCase for classes). Emphasize clarity over brevity.
- **Imports:** Use absolute imports exclusively. Group standard library, third-party, and local imports.
- **Documentation:** Google-style docstrings are mandatory for all public classes, methods, and functions.

### 2. Type Safety (`python-type-safety`)
- **Strict Typing:** All function signatures must have complete type hints.
- **Tooling:** Use `mypy` or `pyright` configured for strict type checking (`strict = true`). No untyped definitions allowed in production code.

### 3. Error Handling & Validation (`python-error-handling`)
- **Validation:** Use Pydantic for robust request/response validation and type safety at the API and agent boundaries.
- **Exceptions:** Implement explicit, custom exception hierarchies. Avoid bare `except Exception:` blocks.

### 4. Testing (`python-testing-patterns`)
- **Tooling:** Pytest.
- **Strategy:** Leverage fixtures for setup/teardown (especially for MongoDB and Qdrant mocks). Prioritize testing agent routing and API validation.

### 5. Project Structure (`python-project-structure`)
- **Modularity:** Keep agent logic separate from API routing and data access layers.

## 🏃‍♂️ Sprint 1: Execution Plan (Infrastructure & Foundation)
**Goal:** Establish the monorepo structure, Docker environment, and base FastAPI configuration.

### 📋 Task Checklist
- [ ] **T001: Repository Setup** — Create `ai/`, `bot/`, and `web/` directories.
- [ ] **T002: Docker Compose** — Create `docker-compose.yml` with health checks.
- [ ] **T003/T004: DB Setup** — Configure MongoDB and Qdrant containers.
- [ ] **T005: FastAPI Base** — Initialize `ai/app/main.py` and `ai/app/config.py`.
- [ ] **T006: Environment** — Create `.env.example`.
- [ ] **T008: Git Strategy** — Ensure `main`, `develop`, and `feature/` branches are ready.

### 🛠 Implementation Guide

#### 1. Folder Structure
Follow the structure in `MARKA_AI_Technical_Document.md` Section 10.1. Keep `ai/` logic separate from `bot/` and `web/`.

#### 2. Model Mapping (Smart Orchestrator)
Ensure `ai/app/config.py` uses:
- Orchestrator: `google/gemini-3-flash`
- Content Agent: `google/gemini-3.1-pro`
- Fast Workers: `google/gemini-3.1-flash-lite`

#### 3. Inter-Component Auth
Implement the `X-API-Token` header validation in `ai/app/middleware/auth.py`. 

#### 4. Startup Sequence
The `bot` and `web` services MUST use `depends_on` with `service_healthy` conditions for the `fastapi` service.

---
## 🧠 LLM Implementation Rules

### 1. Model Naming Convention (LiteLLM + ADK)
When using the `LLMService` to get models, follow these string formats in `.env`:
- **Google AI Studio (Primary):** MUST use the `gemini/` prefix (e.g., `gemini/gemini-3-flash-preview`).
- **Google Cloud Vertex:** Use the `vertex_ai/` prefix.
- **Gemini 3 Series:** Always include the `-preview` suffix (e.g., `gemini-3-flash-preview`) until they reach General Availability.

### 2. Environment Variable Priority
- **API Key:** Use `LLM_API_KEY` in the root `.env`.
- **Internal Mapping:** `LLMService` automatically maps this to `GEMINI_API_KEY` and `GOOGLE_API_KEY` for ADK/LiteLLM compatibility.

### 3. Google ADK "Runner" Pattern
ADK agents cannot be run with a simple `.run()` method. You MUST use the `Runner` with a `SessionService`.

**Correct Pattern:**
```python
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# 1. Setup
session_service = InMemorySessionService()
llm_service = LLMService()

# 2. Initialize Runner
async with Runner(
    app_name="MarkaAI",
    agent=my_agent, 
    session_service=session_service,
    auto_create_session=True
) as runner:
    # 3. Format input using official google-genai types
    message = types.Content(
        role="user", 
        parts=[types.Part.from_text(text="Your message here")]
    )
    
    # 4. Stream results
    async for event in runner.run_async(
        user_id="user_id",
        session_id="session_id",
        new_message=message
    ):
        if hasattr(event, "text") and event.text:
            print(event.text)
```

---
## 🤖 AI Interaction Guidelines
- **Always Read the Skills:** Before making architectural decisions or writing complex logic, consult the relevant skill markdown files in `.agents/skills/`.
- **Align with v1 Architecture:** Ensure all new code respects the defined split between Orchestrator, RAG, Chatbot, and Content agents. Do not blur the lines of responsibility.
- **Validate Everything:** After code changes, ensure `ruff check .` and type checks pass. Maintain Pydantic validation across all system boundaries.
- **Language Nuance:** When working on the Content Agent prompts, explicitly optimize for the Egyptian Arabic dialect as specified in the product vision.
