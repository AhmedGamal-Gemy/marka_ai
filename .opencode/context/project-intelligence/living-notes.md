<!-- Context: project-intelligence/notes | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->

# Living Notes

> Active issues, technical debt, open questions, and insights that don't fit elsewhere. Keep this alive.

## Quick Reference

- **Purpose**: Capture current state, problems, and open questions
- **Update**: Weekly or when status changes
- **Archive**: Move resolved items to bottom with status

## Technical Debt

| Item | Impact | Priority | Mitigation |
|------|--------|----------|------------|
| [Debt item] | [What risk it creates] | [High/Med/Low] | [How to manage] |

### Technical Debt Details

**[Debt Item]**  
*Priority*: [High/Med/Low]  
*Impact*: [What happens if not addressed]  
*Root Cause*: [Why this debt exists]  
*Proposed Solution*: [How to fix it]  
*Effort*: [Small/Medium/Large]  
*Status*: [Acknowledged | Scheduled | In Progress | Deferred]

## Open Questions

| Question | Stakeholders | Status | Next Action |
|----------|--------------|--------|-------------|
| [Question] | [Who needs to decide] | [Open/In Progress] | [What needs to happen] |

### Open Question Details

**[Question]**  
*Context*: [Why this question matters]  
*Stakeholders*: [Who needs to be involved]  
*Options*: [What are the possibilities]  
*Timeline*: [When does this need resolution]  
*Status*: [Open/In Progress/Blocked]

## Known Issues

| Issue | Severity | Workaround | Status |
|-------|----------|------------|--------|
| [Issue] | [Critical/High/Med/Low] | [Temporary fix] | [Known/In Progress/Fixed] |

### Issue Details

**[Issue Title]**  
*Severity*: [Critical/High/Med/Low]  
*Impact*: [Who/what is affected]  
*Reproduction*: [Steps to reproduce if applicable]  
*Workaround*: [Temporary solution if exists]  
*Root Cause*: [If known]  
*Fix Plan*: [How to properly fix]  
*Status*: [Known/In Progress/Fixed in vX.X]

## Insights & Lessons Learned

### What Works Well
- [Positive pattern 1] - [Why it works]
- [Positive pattern 2] - [Why it works]

### What Could Be Better
- [Area for improvement 1] - [Why it's a problem]
- [Area for improvement 2] - [Why it's a problem]

### Lessons Learned
- **NEVER hardcode git user.name/user.email** — Always use `gh api user` to get the authenticated GitHub identity. Use `git commit --amend --author="$(gh api user --jq '.login') <$(gh api user --jq '.login')@users.noreply.github.com>"` instead. The repo has no local git identity configured by design.
- **Google ADK reads API keys from env vars** — `GEMINI_API_KEY` or `GOOGLE_API_KEY` must be set in the environment. Passing `api_key` to the `Gemini()` constructor does NOT work. `LLMService._ensure_environment_keys()` handles this mapping from `LLM_API_KEY`.

## Patterns & Conventions

### Code Patterns Worth Preserving
- **ADK Agent Pattern** — `LLMService` → `Agent(output_schema)` → `Runner` → `model_validate_json()`. See `technical-domain.md` for full template.
- **Email Schema** — `ContentResponse` → `MarketingEmail` → `EmailPart` with `EmailStrategy` enum. Structured, typed, extensible.
- **Settings DI** — All agents accept `settings=None`, default to `get_settings()`. Enables test injection.

### Gotchas for Maintainers
- **ADK Gemini class** — Does NOT use `api_key` constructor param. Must set env vars before instantiation.
- **LLMService lru_cache** — `get_settings()` is cached. If you change `.env`, you need to restart the process.
- **Integration tests** — Require `LLM_API_KEY` in `.env`. Will fail without a valid Gemini API key.

## Active Projects

| Project | Goal | Owner | Timeline |
|---------|------|-------|----------|
| Sprint 2 — AI Layer | Build all 4 agents + LLM infra | Ahmed + Yomna | W3-5 |

### Sprint 2 Status (2026-03-29)

| Task | Description | Owner | Status |
|------|-------------|-------|--------|
| T009 | LLMService | Ahmed | ✅ Done |
| T010 | LLM Provider Config | Ahmed | ✅ Done |
| T011 | Orchestrator Agent | Ahmed | ✅ Done |
| T013 | Content Agent | Ahmed | ✅ Done |
| T015 | Agent Prompts Design | Ahmed | ❌ Blocked (needs T012+T014) |
| T012 | RAG Agent | Yomna | ❌ Not started |
| T014 | Chatbot Agent | Yomna | ❌ Not started |
| T016 | Rate Limiting | Shared | ❌ Not started |

**Ahmed's Sprint 2 is complete** (T009, T010, T011, T013). T015 blocked by Yomna.

## Archive (Resolved Items)

Moved here for historical reference. Current team should refer to current notes above.

### Resolved: [Item]
- **Resolved**: [Date]
- **Resolution**: [What was decided/done]
- **Learnings**: [What we learned from this]

## Onboarding Checklist

- [ ] Review known technical debt and understand impact
- [ ] Know what open questions exist and who's involved
- [ ] Understand current issues and workarounds
- [ ] Be aware of patterns and gotchas
- [ ] Know active projects and timelines
- [ ] Understand the team's priorities

## Related Files

- `decisions-log.md` - Past decisions that inform current state
- `business-domain.md` - Business context for current priorities
- `technical-domain.md` - Technical context for current state
- `business-tech-bridge.md` - Context for current trade-offs
