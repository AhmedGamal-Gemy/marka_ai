# Marka AI

> AI-powered marketing automation for Egyptian & MENA businesses — Arabic-first, built for SMEs.

---

## Stack

| Layer | Tech | Version | Owner |
|---|---|---|---|---|
| Frontend | React + Next.js | Node 22 | Frontend teammate |
| API Gateway | Express (Node.js) — auth, CRUD, DB, streaming | Node 22 | Frontend teammate |
| AI Backend | FastAPI (Python) — agents, RAG, LLM | Python 3.13 | AI engineer |
| Agent Orchestration | Google ADK | Latest | AI engineer |
| Database | PostgreSQL 17 | Latest | Shared (Express owns schema) |
| Cache / Queues / Streaming | Redis 8 | Latest | Shared |
| Vector Store | Pinecone | Latest | AI engineer |
| Web Scraping | Scrapling | Latest | AI engineer |
| Docs | Zensical | Latest | Both |

---

## Service Port Mappings

| Service | Host Port | Container Port | Internal URL |
|---------|-----------|----------------|-------------|
| Frontend (Next.js) | 5173 | 3000 | `http://frontend:3000` |
| Backend (Express) | 3000 | 3000 | `http://backend:3000` |
| AI Backend (FastAPI) | 8001 | 8000 | `http://ai:8000` |
| PostgreSQL | 5432 | 5432 | `postgres://postgres:5432/marka_db` |
| Redis | 6380 | 6379 | `redis://redis:6379` |

**Important**:
- Host ports are used when accessing services from your machine (localhost:5173, etc.)
- Container ports are used for inter-service communication inside Docker network
- AI Backend is accessed on port 8001 from host, but internally on port 8000

---

## Quick Start

### 0. Environment Setup
```bash
# Copy root .env.example to .env and configure values
cp .env.example .env
# Edit .env with your actual keys and values
```

Service-specific `.env.example` files exist in:
- `backend/.env.example` (Express)
- `frontend/.env.example` (React)
- `ai/.env.example` (FastAPI)

### 1. Docker Compose (Recommended - All Services)

#### Linux / macOS / WSL2
```bash
docker compose up -d
```

#### Windows (Docker Desktop)
**IMPORTANT**: On Windows, always run Docker Compose from WSL2.

```powershell
# Open WSL2 and navigate to project
wsl
cd /mnt/d/AHMED_DATA/Projects/marka_ai
docker compose up -d
```

Or from PowerShell in one command:
```powershell
wsl -d Ubuntu -- cd /mnt/d/AHMED_DATA/Projects/marka_ai && docker compose up -d
```

### 2. Individual Services (Development)

#### API Gateway (Express)
```bash
cd backend
npm install
npm run dev          # runs on :3000
```

#### AI Backend (FastAPI)
```bash
cd ai
uv sync
uv run fastapi dev   # runs on :8000 — internal only, not public
```

#### Frontend (React)
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
- FastAPI is internal only — never exposed to internet.
- Every request to FastAPI must carry `X-Service-Key` and `Authorization` headers.
- No route in either service is unprotected.
- React never calls FastAPI directly. React never calls `fetch` outside of `src/api/`.

Full project reference → [`CLAUDE.md`](./CLAUDE.md)

---

## Project Docs

| File | Purpose |
|---|---|
| [`CLAUDE.md`](./CLAUDE.md) | Complete development guide for Claude Code |
| [`DEPLOYMENT.md`](./DEPLOYMENT.md) | CI/CD pipeline and VPS deployment |
| [`plan.md`](./plan.md) | Phased roadmap with tasks per owner |
| [`feature_log.md`](./feature_log.md) | Feature status tracking |
