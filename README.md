# MARKA AI

Autonomous AI Marketing Automation Framework focused on an Arabic-first experience for Egyptian SMEs.

## 🚀 Quick Start (Local Development)

This project uses `uv` for Python package management and Docker Compose for running the infrastructure.

### Prerequisites
- [Docker & Docker Compose](https://www.docker.com/)
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### Setup

1. **Environment Variables**
   Copy the example environment file and fill in your API keys (Gemini, Telegram):
   ```bash
   cp .env.example .env
   ```

2. **Start the Infrastructure**
   This will spin up MongoDB, Qdrant, the FastAPI backend, and dummy containers for the bot and web UI.
   ```bash
   docker compose up --build
   ```

3. **Access the API**
   Once the health checks pass, FastAPI will be available at:
   - Docs: http://localhost:8080/docs
   - Health: http://localhost:8080/health

## 🏗 Architecture
- **AI Layer:** FastAPI, LiteLLM, Pydantic.
- **Databases:** MongoDB 8.0 (State), Qdrant v1.17.0 (Vector Store).
- **LLMs:** Google Gemini (Smart Orchestrator Strategy using `gemini-3-flash` and `gemini-3.1-pro`).

See `MARKA_AI_Technical_Document.md` for full architectural details.
