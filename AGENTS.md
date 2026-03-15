# Marka AI

> AI-powered marketing automation for Egyptian & MENA businesses — Arabic-first, built for SMEs.

---

## Stack

| Layer | Tech | Owner |
|---|---|---|
| Frontend | React | Frontend teammate |
| API Gateway | Express (Node.js) — auth, CRUD, DB, streaming | Frontend teammate |
| AI Backend | FastAPI (Python) — agents, RAG, LLM | AI engineer |
| Agent Orchestration | Google ADK | AI engineer |
| Database | PostgreSQL | Shared (Express owns schema) |
| Cache / Queues / Streaming | Redis | Shared |
| Vector Store | Pinecone | AI engineer |
| Web Scraping | Scrapling | AI engineer |
| Docs | Zensical | Both |

---

## Quick Start

### 1. API Gateway (Express)
```bash
cd backend
npm install
npm run dev          # runs on :3000
```

### 2. AI Backend (FastAPI)
```bash
cd ai
uv sync
uv run fastapi dev   # runs on :8000 — internal only, not public
```

### 3. Frontend (React)
```bash
cd frontend
npm install
npm run dev          # runs on :5173
```

---

## Docs

```bash
zensical serve    # preview docs at localhost:8080
zensical build    # generate static site into /docs
```

> API reference is fully auto-generated from code — never edit `/docs` manually.

---

## Key Rules (read before writing any code)

- All Express routes live under `/api/v1/` — no exceptions.
- FastAPI is internal only — never exposed to the internet.
- Every request to FastAPI must carry `X-Service-Key` and `X-User-ID` headers.
- No route in either service is unprotected.
- React never calls FastAPI directly. React never calls `fetch` outside of `src/api/`.

Full architecture rules → [`AGENTS.md`](./AGENTS.md)

---

## Project Docs

| File | Purpose |
|---|---|
| [`AGENTS.md`](./AGENTS.md) | Architecture, ownership, rules — read this first |
| [`plan.md`](./plan.md) | Phased roadmap with tasks per owner |
| [`feature_log.md`](./feature_log.md) | Feature status tracking |