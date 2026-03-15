# Feature Log

Tracks shipped features, in-progress work, and what's planned next.  
Format: `[YYYY-MM-DD] — Description`

---

## Legend

| Symbol | Meaning |
|---|---|
| ✅ | Shipped |
| 🚧 | In progress |
| 📋 | Planned |
| ❌ | Dropped |

---

## Phase 1 — Validation

_Weeks 1–4_

| Status | Feature | Notes |
|---|---|---|
| 📋 | Customer discovery interviews | Target 20+ SME owners |
| 📋 | Competitive audit | Arabic.AI, Qalam.ai, Jasper, ChatGPT |
| 📋 | Stack finalization | ORM, LLM provider decisions |
| 📋 | Repo + CI setup | Lint, test, format pipelines |

---

## Phase 2 — MVP

_Weeks 5–12_

| Status | Feature | Notes |
|---|---|---|
| 📋 | Auth (JWT) | Express layer |
| 📋 | User & team management | CRUD via Express |
| 📋 | Campaign creation & scheduling | Core domain |
| 📋 | AI content generation (Arabic + English) | Content Agent v1 |
| 📋 | Multi-platform publishing (Facebook, Instagram) | Publishing Agent v1 |
| 📋 | Basic analytics dashboard | Campaign performance |
| 📋 | RAG pipeline (brand voice) | Pinecone + embeddings |
| 📋 | Scrapling integration | Competitor content monitoring |

---

## Phase 3 — Pilot

_Weeks 13–20_

| Status | Feature | Notes |
|---|---|---|
| 📋 | Arabic chatbot v1 | Website + WhatsApp |
| 📋 | Publishing Agent (full automation) | Multi-channel dispatch |
| 📋 | Arabic NLP quality tuning | Based on pilot feedback |
| 📋 | Zensical docs | Auto-generated API reference live |

---

## Phase 4 — Scale

_Month 6+_

| Status | Feature | Notes |
|---|---|---|
| 📋 | Predictive Analytics Agent | Customer behavior prediction |
| 📋 | Programmatic Ads Agent | AI-optimized ad bidding |
| 📋 | CRM Agent | Lead tracking + scoring |
| 📋 | White-label offering | For digital agencies |
| 📋 | Enterprise API access | Custom integrations |
| 📋 | Egyptian dialect fine-tuning | Colloquial Arabic model |

---

## Dropped Features

_Nothing dropped yet._

---

## How to Update This File

When you ship something:
1. Change `📋` to `✅` and add the date in the Notes column.
2. If something is in active development, change to `🚧`.
3. If something is cut, move it to **Dropped Features** with a reason.
