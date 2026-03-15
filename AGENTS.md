# AGENTS.md — Marka AI

## What This Project Is

Marka AI is a **marketing automation platform** that lets users create and schedule campaigns, generate AI-written copy and images, publish across multiple channels (email, social, ads), manage brand assets, and track leads.

---

## Architecture

```
React (Frontend)
      │
      │ REST / WebSocket
      ▼
Express (Node.js — API Gateway)
      │
      ├── Auth (JWT)
      ├── CRUD operations
      ├── Input validation
      ├── PostgreSQL  (business data — owns schema & migrations)
      ├── Redis       (sessions, caching)
      │
      │ Internal HTTP (AI tasks only)
      ▼
FastAPI (Python — AI Backend)
      │
      ├── Google ADK Agent Orchestrator
      │     ├── Content Generation Agent  (copy, images)
      │     ├── Publishing Agent          (channel dispatch)
      │     ├── Analytics Agent           (data aggregation)
      │     └── CRM Agent                 (lead tracking)
      │
      ├── RAG Pipeline
      │     ├── Pinecone  (brand assets, campaign history)
      │     └── Embedding model
      │
      ├── Scrapling    (competitor monitoring, content sourcing)
      │
      ├── PostgreSQL  (shared access — reads shared tables, owns AI-specific tables)
      └── Redis       (agent task queues, pub/sub for streaming)
```

**Key relationships:**
- React never calls FastAPI directly. All requests go through Express first.
- Express owns **auth, CRUD, and schema**. FastAPI is an internal service — never exposed to the internet.
- Both Express and FastAPI hit the same PostgreSQL instance. Express owns shared tables (migrations, writes). FastAPI reads shared tables and writes only to its own AI-specific tables (e.g. `agent_run_logs`, `generation_history`).
- Agent progress is streamed back to React via Redis pub/sub → Express WebSocket.
- Redis is **not a source of truth** — cache and queues only.
- Pinecone is FastAPI-only. Express never touches it.

---

## Commands

### Express Backend — `npm`

```bash
npm install
npm run dev
npm test
npm test -- foo.test.ts   # single file
npm run lint
npm run format
npm run build
```

### FastAPI AI Backend — `uv`

```bash
uv sync
uv run fastapi dev
uv run pytest
uv run pytest tests/foo.py
uv run pytest tests/foo.py::test_bar
uv run pytest --cov
uv run ruff check .
uv run ruff format .
uv run pyright
```

### Frontend — `npm`

```bash
npm install
npm run dev
npm test
npm run build
npm run lint
```

### Documentation — Zensical

```bash
zensical build    # generate static docs site
zensical serve    # preview docs locally
```

---

## Layer Responsibilities (do not cross these lines)

| Concern               | Express        | FastAPI          |
|-----------------------|----------------|------------------|
| Auth / JWT            | ✅ owns it      | ❌ never          |
| CRUD (campaigns etc.) | ✅ owns it      | ❌ never          |
| DB migrations         | ✅ owns it      | ❌ never          |
| Shared table writes   | ✅              | ❌ never          |
| AI-specific table writes | ❌           | ✅ owns it        |
| AI agent execution    | ❌ never        | ✅ owns it        |
| RAG / Pinecone        | ❌ never        | ✅ owns it        |
| LLM API calls         | ❌ never        | ✅ owns it        |
| Redis (sessions)      | ✅              | ❌                |
| Redis (agent queues)  | ❌              | ✅                |

---

## Project-Specific Rules

### Express Layer

- Route handlers must be thin — logic goes in `src/services/`.
- DB access goes in `src/models/` — never inline in handlers.
- Auth middleware runs before all protected routes. Never re-check tokens inside a handler.
- When delegating to FastAPI: fire-and-forget for async jobs (return a job ID to the client), await for synchronous AI responses.
- Validate all request bodies with Zod before forwarding anything to FastAPI.
- All routes return: `{ success: bool, data: any, error: string | null }`.
- HTTP status codes must be accurate — no `200` with `success: false`.
- **All route handlers must have JSDoc comments.** These are the source for Zensical auto-generated API reference — a missing or vague comment means missing docs.

```typescript
/**
 * Create a new campaign.
 * @route POST /campaigns
 * @param {CampaignCreateSchema} req.body - Campaign creation payload
 * @returns {Campaign} The created campaign object
 * @throws {400} Validation error
 * @throws {401} Unauthorized
 */
```

### FastAPI / ADK Agents

- Each agent lives in `app/agents/<agent_name>/`. One agent per domain.
- Agents never import from each other — all inter-agent calls go through the orchestrator.
- Agent tools that need DB data must use `app/models/` — no raw SQL inline in agent code.
- Agent outputs must be validated with Pydantic before being returned. Never pass raw LLM strings upstream.
- All direct LLM API calls (outside ADK) go in `app/llm/`. No scattered `openai.chat.completions.create()` calls.
- **Every public function, agent tool, and Pydantic schema must have a Google-style docstring.** Zensical generates the entire Python API reference from these — a missing docstring means a gap in the docs.

```python
def retrieve_brand_context(user_id: int, query: str) -> list[Document]:
    """Retrieve relevant brand documents for a given query.

    Args:
        user_id: The ID of the user whose brand assets to search.
        query: Natural language query to match against brand assets.

    Returns:
        List of matching Document objects ranked by relevance.

    Raises:
        PineconeQueryError: If the vector search fails.
    """
```

### RAG Pipeline

- All embedding and Pinecone logic lives in `app/rag/`.
- Pinecone namespace convention: `brand-assets`, `campaigns`, `leads`.
- **Always filter by `user_id` metadata** in every Pinecone query — multi-tenant system.
- Never embed raw user input. Sanitize and chunk first via `app/rag/chunker.py`.

### Scrapling

- All scraping logic lives in `app/scraping/`. Never scatter scraping calls across agents.
- Scrapling is used exclusively for: competitor content monitoring, market signal gathering, and lead enrichment. It is never used to scrape user-owned platforms (use their APIs instead).
- Always respect `robots.txt` and rate-limit scraping tasks — run them as background jobs via Redis queue, never in the request/response cycle.
- Scraped data must be cleaned and validated before being passed to agents or stored in the DB.
- Scrapling tasks are triggered by the CRM Agent and Analytics Agent only.

### Database

- Express uses an ORM (Prisma or Sequelize — pick one, be consistent) for all shared table access.
- FastAPI uses SQLAlchemy for its own AI-specific tables and read-only access to shared tables.
- Raw SQL in FastAPI only for complex analytics aggregations.
- All migrations live in the Express layer. FastAPI never runs `alembic upgrade` on shared tables.

### Redis

- Key naming: `{entity}:{id}:{purpose}` — e.g., `campaign:42:status`, `user:7:session`.
- Always set `EXPIRE` on every key. No indefinite keys.
- Express key prefix: `session:`, `cache:`.
- FastAPI key prefix: `queue:agent:`, `stream:`.

---

## Documentation (Zensical)

- Config file: `zensical.toml` at the project root.
- Output: `docs/` folder — do not manually edit files inside it, they are auto-generated.
- Source of truth for API reference is **always the code** (JSDoc for Express, Google-style docstrings for FastAPI) — never write API docs by hand.
- Run `zensical build` before every PR that touches public functions, routes, schemas, or agent tools.
- Docs cover three sections: Express API reference, FastAPI/Agent reference, and Architecture (written manually in `docs-src/`).

---

## What Not To Do

- ❌ Don't expose FastAPI to the public internet — internal service only.
- ❌ Don't put auth logic in FastAPI — Express owns that.
- ❌ Don't run DB migrations from FastAPI.
- ❌ Don't write to shared tables from FastAPI.
- ❌ Don't call Pinecone from Express.
- ❌ Don't let ADK agents return unvalidated strings to the API layer.
- ❌ Don't create a new LLM client per request — instantiate once at startup.
- ❌ Don't store secrets in committed `.env` files.
- ❌ Don't write API reference docs manually — let Zensical generate them.
- ❌ Don't merge code with missing or placeholder docstrings on public functions.

---

## Directory Structure (intended)

```
marka-ai/
├── backend/               # Express — API gateway
│   └── src/
│       ├── routes/        # Thin route handlers (JSDoc on every handler)
│       ├── services/      # Business logic
│       ├── models/        # DB access (ORM)
│       ├── middleware/    # Auth, validation, error handling
│       └── schemas/       # Zod validation schemas
│
├── ai/                    # FastAPI — AI backend
│   └── app/
│       ├── agents/        # One subdirectory per ADK agent
│       ├── api/           # FastAPI route handlers (thin)
│       ├── llm/           # Direct LLM API call wrappers
│       ├── rag/           # Embedding, chunking, Pinecone queries
│       ├── scraping/      # All Scrapling logic (competitor monitoring, lead enrichment)
│       ├── services/      # AI business logic
│       ├── models/        # SQLAlchemy models + DB access
│       └── schemas/       # Pydantic models (validated agent I/O)
│
├── frontend/              # React
│   └── src/
│       ├── api/           # All fetch/axios calls (never in components)
│       ├── components/
│       ├── hooks/         # Shared hooks incl. useAgentStream
│       └── store/         # Global state
│
├── docs/                  # Auto-generated by Zensical — do not edit manually
├── docs-src/              # Hand-written architecture & guide pages
├── zensical.toml          # Zensical config
└── AGENTS.md
```
