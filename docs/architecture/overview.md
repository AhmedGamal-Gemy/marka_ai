---
title: Architecture Overview
---

# Architecture Overview

Marka AI uses a three-layer architecture designed for scalability and separation of concerns.

## System Architecture

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

## Layer Responsibilities

### Frontend (React + Next.js)
- User interface for all features
- Authentication flow (login, register, JWT management)
- Campaign/content management UI
- Analytics dashboards
- **Never calls FastAPI directly**
- **Never uses `fetch` outside of `src/api/`**

### API Gateway (Express)
- All external API routes under `/api/v1/`
- JWT authentication and authorization
- User CRUD operations
- Campaign/Post CRUD operations
- Database schema ownership (PostgreSQL)
- SSE streaming for agent jobs
- Proxies requests to FastAPI with service key

### AI Backend (FastAPI)
- Internal-only service (never public)
- AI agent orchestration (Google ADK)
- RAG pipeline (Pinecone + embeddings)
- LLM operations and content generation
- Web scraping (Scrapling)
- Requires `X-Service-Key` and `Authorization` headers

## Service Port Mappings

| Service | Host Port | Container Port | Internal URL |
|---------|-----------|----------------|-------------|
| Frontend (Next.js) | 5173 | 3000 | `http://frontend:3000` |
| Backend (Express) | 3000 | 3000 | `http://backend:3000` |
| AI Backend (FastAPI) | 8001 | 8000 | `http://ai:8000` |
| PostgreSQL | 5432 | 5432 | `postgres://postgres:5432/marka_db` |
| Redis | 6380 | 6379 | `redis://redis:6379` |

## Critical Architecture Rules

1. **No unprotected routes** - Every route in both Express and FastAPI requires authentication
2. **Express routes** - All must be under `/api/v1/` path
3. **FastAPI access** - Only through Express, never directly from frontend
4. **Service key validation** - Every FastAPI request must include `X-Service-Key` header
5. **JWT validation** - Every request must include valid `Authorization: Bearer <token>` header
6. **API abstraction** - React should only call endpoints through centralized API layer in `src/api/`

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

## Database Schema Ownership

PostgreSQL schema is owned by Express. FastAPI does not modify database schema directly. Any database changes must go through Express migrations.


