# Marka AI — Development Plan

## Vision

Arabic-first AI marketing automation for Egyptian SMEs. Fill the gap left by global tools (no Arabic dialect support, USD pricing) and regional tools (narrow scope). Target the 82% of Egyptian startups not yet using AI in their marketing.

---

## Who Builds What

| Layer | Owner | Stack |
|---|---|---|
| Frontend (React) | Frontend teammate | React, Zustand/Context, Axios |
| API Gateway | Frontend teammate | Express (Node.js), PostgreSQL, Redis |
| AI Backend | AI engineer | FastAPI (Python), Google ADK, Pinecone, Scrapling |

---

## Target Segments

| Segment | Size | Budget (EGP/mo) | Priority |
|---|---|---|---|
| SMEs | 3.5M+ businesses | 2,000–8,000 | 🔴 Primary |
| E-commerce stores | 2,000+ stores | 10,000–30,000 | 🟡 Secondary |
| Digital agencies | 500+ agencies | 15,000–50,000 | 🟡 Secondary |
| Corporations | 500+ companies | 50,000+ | 🟢 Long-term |

---

## Pricing Tiers

| Plan | Price (EGP/mo) | Key Limits |
|---|---|---|
| Starter | 3,000 | 100 posts, 1 platform, basic analytics |
| Growth | 12,000 | 500 posts, 3 platforms, chatbot, analytics |
| Enterprise | 40,000+ | Unlimited, all platforms, API access, dedicated support |

---

## Roadmap

### Phase 1 — Validation (Weeks 1–4)
> Goal: Confirm demand before writing a line of code.

- [ ] Customer discovery interviews (target: 20+ Egyptian SME owners)
- [ ] Competitive audit (Arabic.AI, Qalam.ai, Jasper, ChatGPT)
- [ ] Define Arabic dialect requirements (MSA vs Egyptian colloquial)
- [ ] Finalize ORM choice (Prisma or Sequelize)
- [ ] Finalize LLM provider(s)
- [ ] Set up monorepo, CI pipeline (lint + test on every PR)
- [ ] Agree on DB schema for core tables before writing any code

**Deliverables:** Market validation report, customer personas, finalized stack decisions

---

### Phase 2 — MVP Build (Weeks 5–12)
> Goal: A working product that can generate content and publish it.

#### Shared Infrastructure
- [ ] PostgreSQL setup with migration tooling
- [ ] Redis setup (sessions, cache, pub/sub)
- [ ] Environment variable management (no secrets in code)
- [ ] Monorepo scripts: dev, test, lint, build for all three layers

#### Express — Auth & Foundation _(frontend teammate)_
- [ ] **Auth layer 1** — JWT middleware on all protected routes
- [ ] User registration + login endpoints (`/api/v1/auth/register`, `/api/v1/auth/login`)
- [ ] JWT refresh token flow
- [ ] API versioning — all routes under `/api/v1/`
- [ ] Ownership middleware (`owner_id === req.user.id` on every resource)
- [ ] Global error handling middleware
- [ ] Zod validation middleware (request body validation before handlers)
- [ ] `aiService.ts` — single service for all FastAPI calls (with service key headers)
- [ ] SSE endpoint for agent job streaming (`GET /api/v1/jobs/:id/stream`)

#### Express — Core CRUD _(frontend teammate)_
- [ ] **Users** — profile read/update (`/api/v1/users/me`)
- [ ] **Campaigns** — create, read, update, delete, list (`/api/v1/campaigns`)
- [ ] **Posts** — create, read, update, delete, list per campaign (`/api/v1/posts`)
- [ ] **Brand assets** — upload, read, delete (`/api/v1/brand`)
- [ ] **Leads** — create, read, update, list (`/api/v1/leads`)
- [ ] **Platform connections** — store OAuth tokens for Facebook/Instagram (`/api/v1/platforms`)

#### React — Frontend _(frontend teammate)_
- [ ] Project scaffold (routing, global state, API layer)
- [ ] Auth flow (login, register, JWT storage, auto-refresh)
- [ ] Dashboard layout
- [ ] Campaign list + create screens
- [ ] Content editor screen (displays AI-generated content, allows edits)
- [ ] `useAgentStream` hook (consumes SSE, exposes progress + result state)
- [ ] Analytics dashboard (basic charts — campaign performance)
- [ ] Arabic/English UI toggle (RTL support for Arabic)

#### FastAPI — AI Foundation _(AI engineer)_
- [ ] **Auth layer 2** — service key validation middleware on all routes
- [ ] Per-user rate limiting middleware
- [ ] Google ADK orchestrator setup
- [ ] Content Generation Agent v1 (Arabic + English copy)
- [ ] RAG pipeline (Pinecone + embeddings + brand voice context)
- [ ] `POST /ai/content/generate` — synchronous content generation
- [ ] `POST /ai/campaign/create` — async campaign pipeline (returns job_id)
- [ ] Redis pub/sub publisher (agent progress events → `stream:{job_id}`)
- [ ] Scrapling integration (competitor monitoring, background job)

**Deliverables:** End-to-end working prototype — user logs in, creates campaign, AI generates content, posts to Facebook/Instagram

---

### Phase 3 — Pilot (Weeks 13–20)
> Goal: Real customers, real feedback.

#### Express / Frontend _(frontend teammate)_
- [ ] Subscription plan enforcement (check user.plan before allowing actions)
- [ ] Post scheduling UI (calendar view)
- [ ] Multi-platform publishing UI (select channels per post)
- [ ] Lead management screen (list, detail, status updates)
- [ ] Notifications (in-app alerts for completed jobs, publishing results)
- [ ] Basic account settings screen

#### FastAPI _(AI engineer)_
- [ ] Publishing Agent (automated multi-channel dispatch)
- [ ] Analytics Agent (performance data aggregation)
- [ ] Arabic NLP quality review and tuning based on pilot feedback
- [ ] Arabic Chatbot v1 (website + WhatsApp integration)
- [ ] `POST /ai/campaign/analyze` — campaign performance breakdown

#### Both
- [ ] Onboard 5–10 pilot customers
- [ ] Zensical docs live and accurate
- [ ] Error monitoring set up (Sentry or equivalent)

**Deliverables:** Case studies, testimonials, churn/retention baseline

---

### Phase 4 — Scale (Month 6+)
> Goal: 50 paying customers by end of Year 1.

#### Express / Frontend
- [ ] White-label workspace support (agencies serving their own clients)
- [ ] Enterprise API access (external API with separate auth)
- [ ] Billing integration (subscription management)
- [ ] Team collaboration (invite members to a workspace)

#### FastAPI
- [ ] Predictive Analytics Agent
- [ ] Programmatic Ads Agent (AI-optimized bidding)
- [ ] CRM Agent (lead tracking + scoring)
- [ ] Egyptian dialect fine-tuning (colloquial Arabic model)
- [ ] Feedback loop (analytics → content agent auto-improvement)

---

## Year 1 Targets

| Metric | Target |
|---|---|
| Paying customers | 50 |
| ARPU | EGP 6,000/mo |
| Monthly Revenue | EGP 300,000 |
| Annual Revenue | EGP 3,600,000 (~$115K USD) |

---

## Key Risks

| Risk | Owner | Mitigation |
|---|---|---|
| Low SME adoption | Business | Free trials, case studies, education-first marketing |
| Arabic NLP quality | AI engineer | Continuous eval, pilot feedback loop |
| Platform API changes | Frontend teammate | Abstract platform calls behind a service layer |
| Cash flow | Business | EGP pricing, lean team, phased hiring |

---

## Hiring Plan

| Role | When | Owns |
|---|---|---|
| Technical Co-founder (AI) | Day 1 | FastAPI, agents, architecture |
| Frontend teammate | Day 1 | Express, React, DB schema |
| Arabic NLP Specialist | Month 4 | Language model quality |
| Customer Success | Month 6 | Onboarding, retention |