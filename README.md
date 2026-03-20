# Marka AI

> AI-powered marketing automation for Egyptian & MENA businesses — Arabic-first, built for SMEs.

---

## Stack

| Layer | Tech | Owner |
|---|---|---|
| Frontend | React + Next.js (Node 22) | Frontend teammate |
| API Gateway | Express (Node 22) — auth, CRUD, DB, streaming | Frontend teammate |
| AI Backend | FastAPI (Python 3.13) — agents, RAG, LLM | AI engineer |
| Agent Orchestration | Google ADK | AI engineer |
| Database | PostgreSQL 17 | Shared (Express owns schema) |
| Cache / Queues / Streaming | Redis 8 | Shared |
| Vector Store | Pinecone | AI engineer |
| Web Scraping | Scrapling | AI engineer |
| Docs | Zensical | Both |

---

## Quick Start

### Option 1: Docker (Recommended - All Services)

#### Linux / macOS / WSL2
```bash
# Start all services with one command
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

#### Windows (PowerShell + WSL2)
**IMPORTANT**: On Windows, Docker Compose works best from WSL2 due to path and file system issues.

```powershell
# Option 1: Open WSL and run there
wsl

# Then inside WSL:
cd /mnt/d/AHMED_DATA/Projects/marka_ai
docker compose up -d
```

```powershell
# Option 2: Single command from PowerShell
wsl -d Ubuntu -- cd /mnt/d/AHMED_DATA/Projects/marka_ai && docker compose up -d
```

**Check if WSL2 is installed**:
```powershell
wsl --list --verbose
```

If WSL2 is not installed, run:
```powershell
wsl --install
```

| Service | Host Port | Container Port | URL |
|---------|-----------|----------------|------|
| Frontend | 5173 | 3000 | http://localhost:5173 |
| Backend API | 3000 | 3000 | http://localhost:3000/health |
| AI Backend | 8001 | 8000 | http://localhost:8001/health |
| PostgreSQL | 5432 | 5432 | localhost:5432 |
| Redis | 6380 | 6379 | localhost:6380 |

**Note**: Services communicate internally using container ports (e.g., `http://ai:8000`). Access from host uses host ports.

### Option 2: Individual Services (Development)

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

Full architecture rules → [`AGENTS.md`](./AGENTS.md)

---

## Project Docs

| File | Purpose |
|---|---|
| [`CLAUDE.md`](./CLAUDE.md) | Complete development guide for Claude Code |
| [`AGENTS.md`](./AGENTS.md) | Architecture, ownership, rules — read this first |
| [`DEPLOYMENT.md`](./DEPLOYMENT.md) | CI/CD pipeline and VPS deployment |
| [`plan.md`](./plan.md) | Phased roadmap with tasks per owner |
| [`feature_log.md`](./feature_log.md) | Feature status tracking |

---

## Environment Setup

```bash
# Copy root .env.example to .env and configure values
cp .env.example .env

# Service-specific env files (optional)
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
cp ai/.env.example ai/.env
```

Required environment variables:
- `JWT_SECRET` - Must be identical across all services
- `AI_SERVICE_KEY` - Service key for Express → FastAPI communication
- `POSTGRES_PASSWORD` - PostgreSQL database password
- `PINECONE_API_KEY` - Pinecone vector database key
- `OPENAI_API_KEY` - OpenAI API key

---

## Testing

### All Services (Docker)
```bash
docker compose up -d
docker compose ps
docker compose logs -f
```

### Individual Services
```bash
# Backend
cd backend && npm test

# Frontend
cd frontend && npm test

# AI Backend
cd ai && uv run pytest
```

---

## Health Checks

All services have health checks:
- Backend: http://localhost:3000/health
- Frontend: http://localhost:5173
- AI Backend: http://localhost:8001/health
- PostgreSQL: Database connection
- Redis: PING command

---

## Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   React     │────────>│  Express    │────────>│  FastAPI    │
│  Frontend   │         │   Gateway   │         │   AI Layer  │
└─────────────┘         └─────────────┘         └─────────────┘
                                │                       │
                                ▼                       ▼
                         ┌─────────────┐         ┌─────────────┐
                         │ PostgreSQL  │         │  Pinecone   │
                         │             │         │  Vector DB  │
                         └─────────────┘         └─────────────┘
                                │
                                ▼
                         ┌─────────────┐
                         │    Redis    │
                         │ Cache/Queue │
                         └─────────────┘
```

- **Express** owns the database schema and handles all external requests
- **FastAPI** is internal-only for AI operations (agents, RAG, LLM)
- **React** only talks to Express, never to FastAPI directly
