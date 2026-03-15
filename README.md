# Marka AI

> AI-powered marketing automation platform for Egyptian & MENA businesses — Arabic-first, built for SMEs.

---

## Stack

| Layer | Tech |
|---|---|
| Frontend | React + Next.js |
| API Gateway | Express (Node.js) — auth, CRUD, validation |
| AI Backend | FastAPI (Python) — agents, RAG, LLM |
| Agent Orchestration | Google ADK |
| Database | PostgreSQL |
| Cache / Queues | Redis |
| Vector Store | Pinecone |
| Web Scraping | Scrapling |
| Documentation | Zensical |
| Package Manager (AI) | uv |
| Package Manager (Backend) | npm |

---

## Quick Start

### Prerequisites
- Node.js 18+ (for backend and frontend)
- Python 3.11+ (for AI backend)
- uv package manager (for Python)
- PostgreSQL (running locally or via Docker)
- Redis (running locally or via Docker)

### 1. Set Up Environment Files
```bash
# Backend
cd backend && cp .env.example .env && npm install

# AI Backend
cd ai && uv sync && cp .env.example .env

# Frontend
cd frontend && cp .env.example .env && npm install
```

### 2. Start Services

**Option A: Run all services separately**
```bash
# Terminal 1: Backend
cd backend && npm run dev

# Terminal 2: AI Backend
cd ai && uv run fastapi dev

# Terminal 3: Frontend
cd frontend && npm run dev

# Terminal 4: Docs
zensical serve
```

**Option B: Use Docker Compose** (Coming soon)
```bash
docker-compose up -d
```

---

## Configuration

### Environment Variables

Each service has its own `.env` file:
- `backend/.env` - Express API configuration
- `ai/.env` - FastAPI AI backend configuration
- `frontend/.env` - React frontend configuration

### Database Setup

```bash
# Using PostgreSQL
createdb marka_ai

# Or using Docker
docker run --name marka-postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```

### Redis Setup

```bash
# Using Docker
docker run --name marka-redis -p 6379:6379 -d redis:alpine
```

---

## Documentation

```bash
zensical serve    # preview docs locally at localhost:8000
zensical build    # generate static site into /docs
```

> API reference is fully auto-generated from code — never edit `/docs` manually.

---

## Project Docs

| File | Purpose |
|---|---|
| [`AGENTS.md`](./AGENTS.md) | Architecture rules & coding guidelines |
| [`plan.md`](./plan.md) | Phased roadmap and feature planning |
| [`feature_log.md`](./feature_log.md) | Feature tracking and changelog |
| [`CHANGELOG.md`](./CHANGELOG.md) | Version history and release notes |
| [`README.md`](./README.md) | This file — project overview and quick start |

---

## License

MIT License — see LICENSE file for details

---

## Contributing

1. Read `AGENTS.md` for coding guidelines
2. Follow the roadmap in `plan.md`
3. Update `feature_log.md` when shipping features
4. Update `CHANGELOG.md` for each release

---

## Support

For questions or issues, please open an issue on GitHub.

---

## Roadmap

- **Phase 1** (Validation): Customer discovery, stack finalization, CI setup
- **Phase 2** (MVP): Auth, user management, AI content generation, campaigns, analytics
- **Phase 3** (Pilot): Onboarding 5-10 customers, Arabic NLP tuning, automated publishing
- **Phase 4** (Scale): Predictive analytics, CRM, programmatic ads, white-labeling

See [`plan.md`](./plan.md) for detailed roadmap.
