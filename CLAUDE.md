# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start with Docker

### Linux / macOS / WSL2

**The fastest way to run all services:**

```bash
docker compose up -d
```

This will start:
- Frontend (React) on http://localhost:5173
- Backend API (Express) on http://localhost:3000
- AI Backend (FastAPI) on http://localhost:8001
- PostgreSQL database on localhost:5432
- Redis cache on localhost:6380

### Windows (Docker Desktop)

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

**Why WSL2?**
- Docker Desktop uses WSL2 backend on Windows
- Running `docker compose` from PowerShell causes build context and path issues
- WSL2 provides proper Linux filesystem for Docker builds

**Check if WSL2 is installed**:
```powershell
wsl --list --verbose
```

If WSL2 is not installed, run:
```powershell
wsl --install
```

## Project Overview

Marka AI is an Arabic-first AI marketing automation platform for Egyptian and MENA SMEs. It uses a three-layer architecture:

- **Frontend**: React/Next.js (port 5173 externally, 3000 internally)
- **API Gateway**: Express.js (Node.js, port 3000) — handles auth, CRUD, database, streaming
- **AI Backend**: FastAPI (Python, port 8001 externally, 8000 internally) — internal-only service for agents, RAG, LLM operations

**Critical**: FastAPI is never exposed to internet. All requests go through Express, which proxies to FastAPI.

## Service Port Mappings

| Service | Host Port | Container Port | Internal Access |
|---------|-----------|----------------|----------------|
| Frontend (Next.js) | 5173 | 3000 | `http://frontend:3000` |
| Backend (Express) | 3000 | 3000 | `http://backend:3000` |
| AI Backend (FastAPI) | 8001 | 8000 | `http://ai:8000` |
| PostgreSQL | 5432 | 5432 | `postgres://postgres:5432/marka_db` |
| Redis | 6380 | 6379 | `redis://redis:6379` |

**Note**: When services communicate within Docker network, use container ports and service names (e.g., `http://ai:8000`). When accessing from host machine, use host ports.

## Common Development Commands

### Backend (Express)
```bash
cd backend
npm install              # Install dependencies
npm run dev             # Start dev server (port 3000)
npm run build           # Compile TypeScript
npm run lint           # Run ESLint
npm test              # Run Jest tests
```

### Frontend (React/Next.js)
```bash
cd frontend
npm install              # Install dependencies
npm run dev             # Start dev server (port 5173)
npm run build           # Build for production
npm run lint           # Run ESLint
npm test              # Run Jest tests
npm run test:e2e      # Run Playwright E2E tests
```

### AI Backend (FastAPI)
```bash
cd ai
uv sync                 # Install dependencies
uv run fastapi dev app/main.py     # Start dev server (port 8000)
uv run fastapi run app/main.py     # Start production server
uv run ruff check .                # Lint with Ruff
uv run pyright                     # Type check with Pyright
uv run pytest --cov                # Run tests with coverage
```

### Running All Services (Docker)
```bash
docker compose up -d       # Start all services
docker compose ps          # Check service status
docker compose logs -f     # View logs
docker compose down        # Stop all services
```

### Testing Single Services
```bash
# Backend
cd backend && npm test

# Frontend
cd frontend && npm test

# AI Backend
cd ai && uv run pytest
```

## Architecture & Ownership

### Three-Layer Architecture

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

### Layer Responsibilities

**Express (API Gateway)** - Owned by Frontend Teammate
- All external API routes under `/api/v1/` (no exceptions)
- JWT authentication and authorization
- User CRUD operations
- Campaign/Post CRUD operations
- Database schema ownership (PostgreSQL)
- SSE streaming for agent jobs
- Proxies requests to FastAPI with service key

**FastAPI (AI Backend)** - Owned by AI Engineer
- Internal-only service (never public)
- AI agent orchestration (Google ADK)
- RAG pipeline (Pinecone + embeddings)
- LLM operations and content generation
- Web scraping (Scrapling)
- Requires `X-Service-Key` and `Authorization` headers on all requests

**React (Frontend)** - Owned by Frontend Teammate
- User interface for all features
- Authentication flow (login, register, JWT management)
- Campaign/content management UI
- Analytics dashboards
- Never calls FastAPI directly
- Never uses `fetch` outside of `src/api/`

### Database Schema Ownership

PostgreSQL schema is owned by Express. FastAPI does not modify database schema directly. Any database changes must go through Express migrations.

## Critical Architecture Rules

1. **No unprotected routes**: Every route in both Express and FastAPI requires authentication
2. **Express routes**: All must be under `/api/v1/` path
3. **FastAPI access**: Only through Express, never directly from frontend
4. **Service key validation**: Every FastAPI request must include `X-Service-Key` header
5. **JWT validation**: Every request must include valid `Authorization: Bearer <token>` header
6. **API abstraction**: React should only call endpoints through centralized API layer in `src/api/`

## Authentication Flow

```
React (Client)
    │
    │ 1. User logs in with email/password
    ▼
Express (/api/v1/auth/login)
    │
    │ 2. Validates credentials, generates JWT
    │    JWT contains: { sub: user_id, email, plan }
    ▼
React stores JWT
    │
    │ 3. Subsequent requests include Authorization: Bearer <JWT>
    ▼
Express validates JWT
    │
    │ 4. If AI operation needed:
    │    - Adds X-Service-Key header
    │    - Forwards Authorization header
    ▼
FastAPI validates both:
    - X-Service-Key (proves caller is Express)
    - Authorization JWT (user identity)
```

## Project Structure

```
marka_ai/
├── backend/                # Express.js API Gateway
│   ├── src/
│   │   ├── index.ts                      # Express app entry
│   │   ├── middleware/
│   │   │   └── auth.ts                  # JWT middleware
│   │   ├── routes/v1/
│   │   │   ├── auth.ts                  # Auth endpoints
│   │   │   └── ...                     # Other v1 routes
│   │   ├── services/
│   │   │   └── aiService.ts             # FastAPI proxy service
│   │   └── __tests__/
│   ├── package.json
│   └── tsconfig.json
│
├── frontend/               # React/Next.js Frontend
│   ├── src/
│   │   ├── api/                        # Centralized API calls
│   │   ├── components/
│   │   └── ...
│   ├── package.json
│   └── next.config.js
│
├── ai/                     # FastAPI AI Backend
│   ├── app/
│   │   ├── __init__.py                 # Required for Python package
│   │   ├── main.py                     # FastAPI app entry
│   │   ├── api/v1/
│   │   │   ├── middleware/
│   │   │   │   └── auth.py             # Service key + JWT validation
│   │   │   └── routes/                # AI endpoints
│   │   ├── agents/                     # AI agent implementations
│   │   ├── llm/                        # LLM integrations
│   │   ├── rag/                        # RAG pipeline
│   │   ├── schemas/                    # Pydantic schemas
│   │   └── services/                   # Business logic
│   ├── tests/
│   ├── pyproject.toml
│   └── uv.lock
│
├── docker/                 # Dockerfiles
│   ├── backend/Dockerfile
│   ├── frontend/Dockerfile
│   └── ai/Dockerfile
│
├── .github/workflows/      # CI/CD pipeline
├── docker-compose.yml      # Service orchestration
├── deploy.sh             # VPS deployment script
├── README.md             # Project overview
├── AGENTS.md            # Architecture & rules (read first)
├── plan.md             # Development roadmap
└── feature_log.md      # Feature tracking
```

## AI Backend Structure (FastAPI)

### Critical Import Pattern
Always use absolute imports starting with `app.`:

```python
# Correct
from app.api.v1.middleware.auth import verify_request
from app.schemas.user import UserCreate

# Incorrect - will fail
from app.middleware.auth import verify_request
from ..middleware.auth import verify_request
```

### Package Initialization
Every directory that should be importable must have `__init__.py`:
- `ai/app/__init__.py`
- `ai/app/api/v1/__init__.py`
- `ai/app/api/v1/middleware/__init__.py`

## CI/CD Pipeline

### Current State
The CI/CD pipeline (`.github/workflows/ci-cd.yml`) is in **phase 1** - it only runs a structure check to verify required files exist.

### Future Phases (Uncomment as code is added)
- **Phase 2**: Lint and test each service (express, react, fastapi)
- **Phase 3**: Build and push Docker images to GitHub Container Registry
- **Phase 4**: Deploy to VPS on push to main branch

### Running CI Locally
```bash
# Run structure check
cd backend && npm run lint && npm test
cd frontend && npm run lint && npm test
cd ai && uv run ruff check . && uv run pytest
```

## Inter-Service Communication

### Express to FastAPI Pattern

Express communicates with FastAPI through a centralized service layer. When implementing new features:

1. **Express routes** (`backend/src/routes/v1/`) handle external API
2. **Express services** (`backend/src/services/`) proxy to FastAPI
3. Always include both headers:
   - `X-Service-Key`: Service authentication (from env var)
   - `Authorization`: User JWT (from client request)

```typescript
// backend/src/services/aiService.ts (example pattern)
const response = await fetch('http://ai:8000/ai/generate', {
  method: 'POST',
  headers: {
    'X-Service-Key': process.env.AI_SERVICE_KEY!,
    'Authorization': request.headers.authorization!,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data)
})
```

## Environment Variables

### Root Configuration

Copy the root `.env.example` to `.env` and configure values:

```bash
cp .env.example .env
# Edit .env with your actual keys and values
```

The root `.env.example` documents all shared environment variables across services:
- `JWT_SECRET` - Must be identical in all services
- `AI_SERVICE_KEY` - Service key for Express → FastAPI communication
- `POSTGRES_*` - PostgreSQL database configuration
- `REDIS_*` - Redis cache/queue configuration
- `OPENAI_API_KEY` - OpenAI API key
- `PINECONE_API_KEY` - Pinecone vector database key

Service-specific `.env.example` files exist in each directory:
- `backend/.env.example` - Express-specific variables
- `frontend/.env.example` - React/Next.js variables
- `ai/.env.example` - FastAPI-specific variables

### Required for Local Development

**Backend (.env)**
```bash
NODE_ENV=development
PORT=3000
JWT_SECRET=your-secret-key
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=marka_user
POSTGRES_PASSWORD=marka_password
POSTGRES_DB=marka_db
REDIS_HOST=localhost
REDIS_PORT=6379
AI_SERVICE_KEY=your-service-key
```

**Frontend (.env)**
```bash
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:3000/api/v1
```

**AI Backend (.env)**
```bash
JWT_SECRET=your-secret-key
AI_SERVICE_KEY=your-service-key
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=marka_user
POSTGRES_PASSWORD=marka_password
POSTGRES_DB=marka_db
REDIS_HOST=localhost
REDIS_PORT=6379
PINECONE_API_KEY=your-pinecone-key
OPENAI_API_KEY=your-openai-key
```

**Never commit .env files.** Use `.env.example` as template.

## Python Development (AI Backend)

### Package Management
Use `uv` for fast Python package management:
```bash
uv sync              # Install dependencies
uv add <package>     # Add dependency
uv remove <package>   # Remove dependency
```

### Code Style
- Ruff for linting (`uv run ruff check .`)
- Pyright for type checking (`uv run pyright`)
- Line length: 88 characters
- Import style: absolute imports only

### Testing
- Pytest with async support: `uv run pytest`
- Coverage: `uv run pytest --cov`
- Test files: `tests/` directory, named `test_*.py`

## TypeScript Development (Backend & Frontend)

### Code Style
- ESLint configured for both backend and frontend
- TypeScript strict mode enabled
- Node.js >= 22 required

### Testing
- Jest for unit tests
- Supertest for API integration tests (backend)
- Playwright for E2E tests (frontend)

## Common Patterns

### Adding New Features

1. **Express Route** → `backend/src/routes/v1/feature.ts`
2. **Express Service** (if AI needed) → `backend/src/services/featureService.ts`
3. **FastAPI Route** → `ai/app/api/v1/routes/feature.py`
4. **FastAPI Schema** → `ai/app/schemas/feature.py`
5. **React Component** → `frontend/src/components/Feature.tsx`
6. **React API Hook** → `frontend/src/api/useFeature.ts`

### Error Handling

**Express**: Return consistent error format
```typescript
res.status(401).json({ success: false, error: 'Unauthorized' })
```

**FastAPI**: Raise HTTPException with detail
```python
raise HTTPException(status_code=401, detail="Unauthorized")
```

### Database Migrations

Since Express owns the schema:
1. Create migration in backend
2. Run migration before FastAPI tries to access new columns
3. FastAPI should only read/write, never modify schema

## Key Files to Read First

1. **AGENTS.md** - Complete architecture rules and ownership
2. **plan.md** - Phased roadmap with tasks
3. **README.md** - Quick start guide
4. **DEPLOYMENT.md** - CI/CD and deployment instructions

## Important Constraints

- FastAPI is **internal only** - never add public-facing routes
- Express owns the database schema - FastAPI never modifies it
- All Express routes must be versioned (`/api/v1/`)
- No route in either service is unprotected
- React never calls FastAPI directly
- All inter-service calls require service key validation
- Never hardcode credentials - always use environment variables

## Skills Available

The project includes Python development skills in `.agents/skills/`:
- `python-project-structure` - Project organization and module architecture
- `python-code-style` - Code quality and style guidelines
- `python-error-handling` - Error handling patterns
- `python-testing-patterns` - Testing best practices
- `python-performance-optimization` - Performance optimization
- `python-type-safety` - Type checking and type hints
- `python-design-patterns` - Design patterns for Python

These skills are automatically loaded when working on AI backend (FastAPI) code.

## Common Issues

### FastAPI Import Errors
**Problem**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Ensure all directories have `__init__.py` and use absolute imports starting with `app.`

### Service Key Validation Failures
**Problem**: FastAPI returns 403 "Invalid service key"

**Solution**: Check that `AI_SERVICE_KEY` environment variable is set identically in both Express and FastAPI services

### JWT Validation Failures
**Problem**: "Invalid or expired token"

**Solution**: Ensure `JWT_SECRET` is set identically in all services and token is properly forwarded in Authorization header

### Port Conflicts
**Problem**: Services fail to start due to port already in use

**Solution**: Check ports 3000 (Express), 5173 (Frontend), 8001 (FastAPI external), 8000 (FastAPI internal), 5432 (PostgreSQL), 6380 (Redis external), 6379 (Redis internal) are available

## Testing the Stack

To verify all services are working:

```bash
# 1. Start all services
docker compose up -d

# 2. Check health endpoints
curl http://localhost:3000/health     # Express
curl http://localhost:8001/health     # FastAPI

# 3. Check auth chain (requires valid JWT)
curl http://localhost:3000/api/v1/hello
```

## Getting Help

- Read AGENTS.md for architecture questions
- Check DEPLOYMENT.md for CI/CD issues
- Review plan.md for feature implementation order
- Use available skills for Python development patterns
