# MARKA AI
**Autonomous AI Marketing Automation Framework**
*v1 Architecture & Technical Document*

> **Internal — Confidential**
> **Last Updated:** March 2026
> **Team:** Ahmed Gamal + Yomna Hadad

---

## 🤖 Agentic Context & Quick Reference
*(Optimized for AI Assistants interacting with this repository)*

- **Primary Goal:** Generate marketing content in **Egyptian Arabic Dialect** for SMEs.
- **Core Architecture:** Two layers — FastAPI (AI Backend) and Telegram/React (Frontend).
- **Tech Stack:** FastAPI, LiteLLM, Qdrant (Vector/RAG), MongoDB (State), `python-telegram-bot`, React.
- **Dependency Management:** Use `uv` for Python environments and dependencies.
- **Authentication:** Inter-component authentication MUST use the `X-API-Token` header (NOT `Authorization: Bearer`).
- **LLM Settings (Smart Orchestrator Strategy):**
  - Orchestrator: `google/gemini-3-flash` (Smart tool caller)
  - Content Agent: `google/gemini-3.1-pro` (Heavy reasoning - Egyptian Arabic)
  - Fast Workers (RAG/Chatbot): `google/gemini-3.1-flash-lite`
  - Embeddings: `google/gemini-embedding-2`
  - Dimensions: **768 dimensions** (CRITICAL: Must match Qdrant configuration).
- **State Management:** In-memory job state is acceptable for v1, but durable logs go to MongoDB.

---

## 1. Product Overview

### 1.1 Vision
An Arabic-first AI assistant that helps Egyptian SMEs create, schedule, and publish marketing content — without needing marketing expertise or English-language tools.

### 1.2 The Problem
| Pain Point | Current Reality | Marka AI Solution |
| :--- | :--- | :--- |
| **Language** | Global tools don't support Egyptian Arabic dialect | Native Arabic-first generation with dialect tuning |
| **Complexity** | SMEs need to learn marketing + tools simultaneously | AI handles strategy, timing, and content automatically |
| **Cost** | USD pricing is prohibitive for Egyptian businesses | EGP pricing, local payment methods |
| **Time** | Business owners are operators, not marketers | Fully automated — from product to published post |

### 1.3 Business Model
| Phase | Timeline | Model | Notes |
| :--- | :--- | :--- | :--- |
| **Phase A (Now)** | MVP — Pilot | Free / Beta | Ahmed + Yomna build, test with 3-5 SMEs |
| **Phase B** | Post-MVP | Subscription (EGP/month)| Starter: 3,000 \| Growth: 12,000 \| Enterprise: 40,000+ |
| **Phase C** | Scale | Multi-tenant SaaS | White-label for agencies, API access |

---

## 2. Team & Responsibilities

### 2.1 Core Team (v1)
| Member | Domain | Responsibilities | Tools |
| :--- | :--- | :--- | :--- |
| **Ahmed** | Orchestration + Integration | Agent orchestration, Content Agent prompts, Telegram bot, Web UI, Publisher logic, API_TOKEN auth | FastAPI, LiteLLM, python-telegram-bot, React, MongoDB |
| **Yomna** | AI + RAG | RAG system (mini-RAG), Chatbot backend endpoints, embeddings + vector store logic | FastAPI, MongoDB, Qdrant, LiteLLM, sentence-transformers |

---

## 3. System Architecture

### 3.1 Two-Layer Architecture (v1)
| Layer | Stack | Responsibilities | Owner |
| :--- | :--- | :--- | :--- |
| **Frontend Layer** | Telegram Bot + React (AI-generated) | User input, display results, publish actions | Ahmed |
| **AI Layer (FastAPI)**| FastAPI + MongoDB + Qdrant + LiteLLM| Agent orchestration, RAG, content generation, state management | Shared |

### 3.2 Inter-Component Authentication
| Connection | Auth Method | Details |
| :--- | :--- | :--- |
| **Frontend -> FastAPI** | `X-API-Token` header | Single token in `.env`, same for Telegram + Web |
| **FastAPI -> MongoDB** | Connection string in `.env` | No auth layer needed for single-tenant v1 |
| **FastAPI -> Qdrant** | Connection string in `.env` | No auth layer needed for local Docker |
| **FastAPI -> LLM** | API key in `.env` | Managed by LiteLLM |
| **FastAPI -> Telegram** | Bot token in `.env` | Standard Telegram Bot API auth |

---

## 4. Agent Architecture

### 4.1 Agent Hierarchy (v1)
| Agent | Owner | Responsibility | v1 Scope |
| :--- | :--- | :--- | :--- |
| **Orchestrator** | Ahmed | Routes requests, manages job state, calls sub-agents | Simple if/else routing |
| **RAG Agent** | Yomna | Retrieves brand voice + product context | mini-RAG: single-product memory |
| **Chatbot Agent**| Yomna | Handles Telegram/Web intent parsing | Basic intents: `/start`, describe, pick, publish |
| **Content Agent**| Ahmed | Generates Arabic marketing copy | 3 caption options, Egyptian dialect tuning |

---

## 5. Tools

### 5.1 Tool Inventory (v1)
| Tool | Used By | Purpose | Owner |
| :--- | :--- | :--- | :--- |
| **FastAPI** | Backend | API routes, middleware, request validation | Shared |
| **MongoDB** | Backend + RAG | Structured data: brand memories, job history | Yomna + Ahmed |
| **Qdrant** | RAG Agent | Vector embeddings for semantic search | Yomna |
| **LiteLLM** | All agents | Unified LLM interface (swap providers via config) | Shared |
| **python-telegram-bot**| Telegram Bot| Handle bot commands, send messages, media | Ahmed |
| **Pydantic** | All agents | Request/response validation, type safety | Shared |
| **Apidog** | API testing | API design, testing, documentation, mocking | Both |
| **Docker** | Deployment | Containerize FastAPI + MongoDB + Qdrant | Ahmed |
| **GitHub** | Version Control | Code hosting, PRs, basic CI | Both |
| **Google Gemini API** | LLM Provider | Primary LLM for Arabic generation + embeddings | Ahmed |

---

## 6. LLM Configuration

### 6.1 Provider-Agnostic via LiteLLM
```python
# ai/config.py -- Smart Orchestrator Strategy
# Orchestrator (Smart Tool Caller): 1,000 RPM / 10,000 RPD
ORCHESTRATOR_MODEL = "google/gemini-3-flash"

# Content Agent (Heavy Reasoning - Egyptian Arabic): 25 RPM / 250 RPD
CONTENT_MODEL      = "google/gemini-3.1-pro"

# Fast Workers (RAG/Chatbot Tasks): 4,000 RPM / 150,000 RPD
RAG_MODEL          = "google/gemini-3.1-flash-lite"
CHATBOT_MODEL      = "google/gemini-3.1-flash-lite"

# Embedding model -- 3,000 RPM / Unlimited RPD
EMBEDDING_MODEL    = "google/gemini-embedding-2"
QDRANT_VECTOR_SIZE = 768

# Global Rate Limiting (Safe for 3.1 Pro quota)
LLM_REQUESTS_PER_MINUTE = 25
MAX_TOKENS_PER_REQUEST  = 2000
```

### 6.2 LLM Provider Strategy (Updated 2026)
| Provider | Model | Pricing (per 1M tokens) | Arabic Support | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **Google Gemini** | `gemini-2.0-flash` | $0.075 input / $0.30 output | Good | **v1 Default** — Fast, generous free tier |
| **Mistral** | `mistral-small-3.1` | $0.20 input / $0.60 output | Good | **v2 Fallback** — Strong reasoning |
| **Groq** | `llama-3.3-70b` | ~$0.05 input / $0.05 output | Decent | **v2 Real-time** — Ultra-fast inference |

---

## 7. State Management & RAG

### 7.1 Dual-Store Strategy
| Store | Purpose | Owner | v2 Plan |
| :--- | :--- | :--- | :--- |
| **MongoDB (Docker)** | Structured data: brand memories, job history, settings | Yomna + Ahmed | Core — add multi-tenant isolation |
| **Qdrant (Docker)** | Vector embeddings for semantic search (RAG) | Yomna | Core — add hybrid search, re-ranking |

**RAG Flow — Synchronous (v1):** No async tasks. No queues. Simple request -> response. (~2-5 seconds)

---

## 8. API Layer (FastAPI)

### 8.1 FastAPI Endpoints (v1)
| Endpoint | Method | Purpose | Owner |
| :--- | :--- | :--- | :--- |
| `/health` | GET | Health check for Docker and monitoring | Shared |
| `/api/v1/chat` | POST | Main chat endpoint (Telegram/Web) | Yomna |
| `/api/v1/generate` | POST | Content generation (captions) | Ahmed |
| `/api/v1/publish` | POST | Publish content to Telegram | Ahmed |
| `/api/v1/rag/search` | POST | RAG semantic search | Yomna |
| `/api/v1/brand` | GET/POST | Brand context management | Yomna |

### 8.2 API Authentication
```python
# ai/middleware/auth.py -- Ahmed owns
import os
from fastapi import HTTPException, Request

API_TOKEN = os.getenv("API_TOKEN")

async def verify_api_token(request: Request):
    """
    Validate the X-API-Token header on all protected endpoints.
    Uses custom header instead of Authorization: Bearer because:
    1. Bearer implies OAuth/JWT, which we don't support in v1
    2. Custom header is explicit -- no ambiguity
    3. Simpler to implement and test
    """
    token = request.headers.get("X-API-Token")
    if not token or token != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing X-API-Token header"
        )
    return token
```

---

## 9. Frontend Layer (Telegram + Web)

### 9.1 Telegram Bot (Primary v1 Frontend)
| Command | Purpose | Owner |
| :--- | :--- | :--- |
| `/start` | Welcome + product description prompt | Ahmed |
| `/new` | Create new campaign | Ahmed |
| `/generate`| Generate captions for product | Ahmed |
| `/publish` | Publish selected caption | Ahmed |
| `/help` | Show available commands | Ahmed |

### 9.2 Web UI (Secondary v1 Frontend)
| Page | Purpose | Owner |
| :--- | :--- | :--- |
| `/` | Landing + quick generate form | Ahmed (AI-gen) |
| `/campaign` | Campaign list + create | Ahmed (AI-gen) |
| `/generate` | Content generation form | Ahmed (AI-gen) |
| `/settings` | Brand voice configuration | Ahmed (AI-gen) |

---

## 10. Repository Structure

### 10.1 Monorepo Structure (v1)
```text
marka_ai/
|-- ai/                          # Python -- uv manages this
|   |-- pyproject.toml           # uv project config
|   |-- app/
|   |   |-- main.py              # FastAPI app entry
|   |   |-- config.py            # Shared config (models, dimensions, rate limits)
|   |   |-- api/v1/              # Route handlers
|   |   |-- middleware/          # auth.py (X-API-Token), rate_limit.py
|   |   |-- agents/              # orchestrator, rag, content, chatbot
|   |   |-- services/            # llm_service, qdrant_service, mongodb_service
|   |   |-- models/              # MongoDB Models (brand_memory, job_history)
|   |   +-- state/               # In-memory job state
|   |-- tests/
|   +-- Dockerfile
|-- bot/                         # Python -- Telegram bot
|   |-- main.py                  # Includes wait_for_api() health check
|   |-- handlers/
|   +-- Dockerfile
|-- web/                         # React -- AI-generated
|   |-- src/
|   |   +-- api/client.ts        # X-API-Token auth client
|   +-- package.json
|-- docker-compose.yml           # Full stack -- health checks + depends_on
|-- README.md                    # How to run locally
+-- GEMINI.md                    # AI assistant contextual instructions
```

---

## 11. Docker & Deployment

### 11.1 Services
| Service | Port | Responsibility |
| :--- | :--- | :--- |
| `fastapi` | `8000` | AI Layer — FastAPI + agents |
| `mongodb` | `27017`| Structured data — brand memories, job history |
| `qdrant` | `6333` | Vector embeddings — RAG semantic search |
| `bot` | — | Telegram bot (runs as background process) |
| `web` | `5173` | React web UI (dev) / static serve (prod) |

---

## 12. GitHub Rules & Workflow

### 12.1 Branch Strategy
| Branch | Rules |
| :--- | :--- |
| `main` | Production. Never push directly. PR + 1 approval required. |
| `develop` | Integration branch. All features merge here first. PR + 1 approval required. |
| `feature/ai/*` | Yomna's AI layer features. Merges to develop. |
| `feature/bot/*`| Ahmed's Telegram bot features. Merges to develop. |
| `feature/web/*`| Ahmed's Web UI features. Merges to develop. |
| `hotfix/*` | Emergency fixes. Branches from main. Merges to main AND develop. |

### 12.2 Commit Convention
Use standard conventional commits (e.g., `feat(ai): ...`, `fix(bot): ...`, `docs: ...`, `chore: ...`).

### 12.3 PR Requirements
- **1 approval** from the other teammate.
- **CI passes** (Lint + test must pass).
- **No console.log / print()** (Remove debug statements before merge).
- **Update docs** (If API changes, update Apidog spec / If Config changes, update this doc).

---

## 13. Open Questions

### 13.1 Resolved Questions
| Question | Resolution | Resolved By |
| :--- | :--- | :--- |
| **Auth header** | Use `X-API-Token` custom header everywhere instead of Bearer. | Document review |
| **Qdrant point IDs**| Use `hashlib.sha256` truncated to 64-bit instead of Python's randomized `hash()`. | Document review |
| **Embedding Dims** | Use 768 dimensions for Google `text-embedding-004`. | Document review |
| **Bot startup race**| Three-layer protection: Docker health checks, `wait_for_api()`, restart on-failure. | Document review |
| **In-memory state** | Accepted for v1. MongoDB `job_history` is durable audit log. Add Redis in v2. | Document review |

### 13.2 Open Questions
- **LLM provider selection:** Which model is best for Arabic dialect? Currently Gemini — should we test Mistral?
- **Telegram vs Web priority:** Should we focus 100% on Telegram for v1, or split effort?
- **Brand voice collection:** How do we collect brand voice from pilot SMEs? Survey? Interview?
- **Pilot recruitment:** How do we find 3-5 Egyptian SMEs for pilot?
- **Arabic dialect tuning:** Should we fine-tune a model or rely on prompt engineering?

---

## Appendix A: Design Decisions Registry
| ID | Problem | Resolution |
| :--- | :--- | :--- |
| **DD-001** | Section 3.3 said `X-API-Token` but Section 8.2 used HTTPBearer | Standardized on `X-API-Token` custom header everywhere |
| **DD-002** | Python's `hash()` is randomized via `PYTHONHASHSEED` | Replaced with `hashlib.sha256` truncated to 64-bit integer |
| **DD-003** | Original doc specified size=1536 but LLM is Google | Changed to 768 dimensions for Google `text-embedding-004` |
| **DD-004** | Bot could start before FastAPI is ready | Three-layer fix: Docker health checks, `wait_for_api()`, restart on-failure |
| **DD-005** | `JobState` loses data on restart | Documented as accepted v1 limitation. MongoDB `job_history` is durable log |

## Document Governance
This document is the **single source of truth** for Marka AI v1 technical decisions. 
- **Architectural / Config changes** MUST be updated here. 
- **Agent prompt changes** MUST be reviewed by both team members.
