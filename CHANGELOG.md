# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-03-26
### Added
- Initial monorepo structure (`ai/`, `bot/`, `web/`).
- `docker-compose.yml` for unified local development.
- Integrated MongoDB (8.0) and Qdrant (v1.17.0) with custom silent health checks.
- Unified `.env` and `.env.example` at the root level.
- `MARKA_AI_Technical_Document.md` for AI agentic context.
- Configured "Smart Orchestrator" LLM strategy using `gemini-3-flash` and `gemini-3.1-pro`.
- Basic FastAPI application initialized with `uv` and `fastapi-cli`.
