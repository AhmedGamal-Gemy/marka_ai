# Marka AI — Development Plan

## Vision

Arabic-first AI marketing automation for Egyptian SMEs. Fill the gap left by global tools (no Arabic dialect support, USD pricing) and regional tools (narrow scope). Target the 82% of Egyptian startups not yet using AI in their marketing.

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
- [ ] Finalize tech stack decisions (ORM choice, LLM provider)
- [ ] Set up project repo, AGENTS.md, CI pipeline

**Deliverables:** Market validation report, customer personas, finalized stack

---

### Phase 2 — MVP Build (Weeks 5–12)
> Goal: Working prototype of core AI content generation.

#### Infrastructure
- [ ] Express API gateway (auth, user management, CRUD)
- [ ] FastAPI AI backend (basic agent setup, LLM integration)
- [ ] PostgreSQL schema (users, campaigns, content)
- [ ] Redis (sessions, caching)
- [ ] React frontend scaffold

#### Core Features
- [ ] **AI Content Generation** — social media posts in Arabic & English
- [ ] **Campaign Management** — create, schedule, track campaigns
- [ ] **Basic Analytics** — post performance dashboard
- [ ] **Multi-platform publishing** — at least Facebook + Instagram for MVP

#### AI Layer
- [ ] Google ADK orchestrator setup
- [ ] Content Generation Agent (v1)
- [ ] RAG pipeline with Pinecone (brand voice context)
- [ ] Scrapling integration for competitive content monitoring

**Deliverables:** Working prototype, internal demo

---

### Phase 3 — Pilot (Weeks 13–20)
> Goal: Real customers, real feedback.

- [ ] Onboard 5–10 pilot customers (SMEs)
- [ ] Arabic NLP quality review and tuning
- [ ] Publishing Agent (automated multi-channel dispatch)
- [ ] Arabic Chatbot v1 (website + WhatsApp)
- [ ] Feedback loop → iterate on content quality
- [ ] Zensical docs live

**Deliverables:** Case studies, testimonials, churn/retention data

---

### Phase 4 — Scale (Month 6+)
> Goal: 50 paying customers by end of Year 1.

- [ ] Predictive Analytics Agent
- [ ] Programmatic Ads Agent (AI-optimized bidding)
- [ ] CRM Agent (lead tracking + scoring)
- [ ] White-label offering for agencies
- [ ] Enterprise tier + API access
- [ ] Arabic dialect model fine-tuning (Egyptian colloquial)
- [ ] Expand to 3 platforms → all major channels

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

| Risk | Mitigation |
|---|---|
| Low SME adoption | Free trials, case studies, education-first marketing |
| Arabic NLP quality | Partner with Arabic AI specialists, continuous eval |
| Global players improving Arabic | Double down on local dialect, pricing, support |
| Cash flow | EGP pricing, lean team, phased hiring |

---

## Hiring Plan

| Role | When | Owns |
|---|---|---|
| Technical Co-founder | Day 1 | Architecture, AI |
| Business Co-founder | Day 1 | Strategy, sales, partnerships |
| Full-Stack Developer | Month 3 | Frontend + backend features |
| Arabic NLP Specialist | Month 4 | Language model quality |
| Customer Success | Month 6 | Onboarding, retention |
