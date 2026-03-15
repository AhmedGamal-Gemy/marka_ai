# Feature Log

Tracks shipped features, in-progress work, and what's planned next.

**Owner key:** 🟦 Frontend teammate (Express + React) · 🟩 AI engineer (FastAPI) · ⬜ Both

---

## Legend

| Symbol | Meaning |
|---|---|
| ✅ | Shipped — add date in Notes |
| 🚧 | In progress |
| 📋 | Planned |
| ❌ | Dropped — move to Dropped section with reason |

---

## Phase 1 — Validation _(Weeks 1–4)_

| Status | Owner | Feature | Notes |
|---|---|---|---|
| 📋 | ⬜ | Customer discovery interviews | Target 20+ SME owners |
| 📋 | ⬜ | Competitive audit | Arabic.AI, Qalam.ai, Jasper, ChatGPT |
| 📋 | ⬜ | ORM decision | Prisma vs Sequelize |
| 📋 | ⬜ | LLM provider decision | OpenAI, Anthropic, or mix |
| 📋 | ⬜ | Monorepo + CI setup | Lint + test on every PR |
| 📋 | ⬜ | Core DB schema agreed | Before any code is written |

---

## Phase 2 — MVP _(Weeks 5–12)_

### Shared Infrastructure

| Status | Owner | Feature | Notes |
|---|---|---|---|
| 📋 | ⬜ | PostgreSQL + Redis setup | |
| 📋 | ⬜ | Environment variable management | No secrets in code |

### Express — Auth & Foundation

| Status | Owner | Feature | Notes |
|---|---|---|---|
| 📋 | 🟦 | JWT middleware | All protected routes |
| 📋 | 🟦 | User registration + login | `/api/v1/auth/register`, `/api/v1/auth/login` |
| 📋 | 🟦 | JWT refresh token flow | |
| 📋 | 🟦 | API versioning (`/api/v1/`) | Applied at router level |
| 📋 | 🟦 | Ownership middleware | `owner_id === req.user.id` |
| 📋 | 🟦 | Global error handling middleware | |
| 📋 | 🟦 | Zod validation middleware | |
| 📋 | 🟦 | `aiService.ts` | Single file for all FastAPI calls |
| 📋 | 🟦 | SSE job stream endpoint | `GET /api/v1/jobs/:id/stream` |

### Express — Core CRUD

| Status | Owner | Feature | Notes |
|---|---|---|---|
| 📋 | 🟦 | Users CRUD | `/api/v1/users/me` |
| 📋 | 🟦 | Campaigns CRUD | `/api/v1/campaigns` |
| 📋 | 🟦 | Posts CRUD | `/api/v1/posts` |
| 📋 | 🟦 | Brand assets CRUD | `/api/v1/brand` |
| 📋 | 🟦 | Leads CRUD | `/api/v1/leads` |
| 📋 | 🟦 | Platform connections | Store OAuth tokens for Facebook/Instagram |

### React — Frontend

| Status | Owner | Feature | Notes |
|---|---|---|---|
| 📋 | 🟦 | Project scaffold | Routing, state, API layer |
| 📋 | 🟦 | Auth flow | Login, register, token storage, auto-refresh |
| 📋 | 🟦 | Dashboard layout | |
| 📋 | 🟦 | Campaign list + create screens | |
| 📋 | 🟦 | Content editor screen | Shows AI output, allows edits |
| 📋 | 🟦 | `useAgentStream` hook | SSE consumption, progress + result state |
| 📋 | 🟦 | Basic analytics dashboard | Campaign performance charts |
| 📋 | 🟦 | Arabic/English UI toggle | RTL support |

### FastAPI — AI Foundation

| Status | Owner | Feature | Notes |
|---|---|---|---|
| 📋 | 🟩 | Service key auth middleware | Validates `X-Service-Key` on all routes |
| 📋 | 🟩 | Per-user rate limiting | Simple, per `user_id` |
| 📋 | 🟩 | ADK orchestrator setup | |
| 📋 | 🟩 | Content Generation Agent v1 | Arabic + English copy |
| 📋 | 🟩 | RAG pipeline | Pinecone + embeddings + brand voice |
| 📋 | 🟩 | `POST /ai/content/generate` | Synchronous |
| 📋 | 🟩 | `POST /ai/campaign/create` | Async, returns job_id |
| 📋 | 🟩 | Redis pub/sub publisher | Agent progress → `stream:{job_id}` |
| 📋 | 🟩 | Scrapling integration | Background job, competitor monitoring |

---

## Phase 3 — Pilot _(Weeks 13–20)_

### Express / Frontend

| Status | Owner | Feature | Notes |
|---|---|---|---|
| 📋 | 🟦 | Subscription plan enforcement | Check user.plan before actions |
| 📋 | 🟦 | Post scheduling UI | Calendar view |
| 📋 | 🟦 | Multi-platform publishing UI | Select channels per post |
| 📋 | 🟦 | Lead management screen | List, detail, status |
| 📋 | 🟦 | In-app notifications | Job completions, publish results |
| 📋 | 🟦 | Account settings screen | |

### FastAPI

| Status | Owner | Feature | Notes |
|---|---|---|---|
| 📋 | 🟩 | Publishing Agent | Multi-channel dispatch |
| 📋 | 🟩 | Analytics Agent | Performance data aggregation |
| 📋 | 🟩 | Arabic NLP tuning | Based on pilot feedback |
| 📋 | 🟩 | Arabic Chatbot v1 | Website + WhatsApp |
| 📋 | 🟩 | `POST /ai/campaign/analyze` | Campaign performance breakdown |

### Both

| Status | Owner | Feature | Notes |
|---|---|---|---|
| 📋 | ⬜ | Zensical docs live | Auto-generated + hand-written architecture pages |
| 📋 | ⬜ | Error monitoring | Sentry or equivalent |

---

## Phase 4 — Scale _(Month 6+)_

### Express / Frontend

| Status | Owner | Feature | Notes |
|---|---|---|---|
| 📋 | 🟦 | White-label workspace support | For agencies |
| 📋 | 🟦 | Enterprise external API | Separate auth system |
| 📋 | 🟦 | Billing integration | Subscription management |
| 📋 | 🟦 | Team collaboration | Invite members to workspace |

### FastAPI

| Status | Owner | Feature | Notes |
|---|---|---|---|
| 📋 | 🟩 | Predictive Analytics Agent | |
| 📋 | 🟩 | Programmatic Ads Agent | AI-optimized bidding |
| 📋 | 🟩 | CRM Agent | Lead tracking + scoring |
| 📋 | 🟩 | Egyptian dialect fine-tuning | Colloquial Arabic model |
| 📋 | 🟩 | Analytics feedback loop | Performance data → content agent |

---

## Dropped Features

_Nothing dropped yet._

---

## How to Update This File

1. Change `📋` to `✅` and add the date in the Notes column when shipped.
2. Change to `🚧` when actively in development.
3. Move dropped features to **Dropped Features** with a one-line reason.