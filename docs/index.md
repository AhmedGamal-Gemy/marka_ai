---
title: Marka AI Documentation
---

# Marka AI Documentation

> AI-powered marketing automation for Egyptian & MENA businesses — Arabic-first, built for SMEs.

---

## Welcome

Welcome to the Marka AI documentation. This site contains everything you need to develop, deploy, and maintain the Marka AI platform.

## Quick Links

### [Getting Started](getting-started/quick-start.md)
Get up and running in 5 minutes.

### [Architecture](architecture/overview.md)
Understand the system design.

### [Environment Variables](reference/environment-vars.md)
Configure environment variables.

### [API Reference](reference/api/index.md)
Auto-generated documentation from Python source code.

### [Agents](agents.md)
AI agents and orchestration.

---

## Project Overview

Marka AI is a three-layer architecture:

1. **Frontend** - React/Next.js user interface
2. **API Gateway** - Express.js REST API
3. **AI Backend** - FastAPI for AI operations

All documentation is auto-generated where possible and maintained in the `docs/` folder.

---

## Contributing

- **CLAUDE.md** in the root contains development guidelines for Claude Code
- **docs/agents.md** contains architecture rules
- Use `uvx zensical serve` to preview changes locally
- Run `uvx zensical build` to generate static docs

---

## Need Help?

- Check [Architecture Overview](architecture/overview.md) for system design
- Review [Quick Start](getting-started/quick-start.md) for setup
- See [Environment Variables](reference/environment-vars.md) for configuration
