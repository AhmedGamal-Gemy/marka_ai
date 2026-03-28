# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.1] - 2026-03-27
### Changed
- Integrated the `Settings` class project-wide using Dependency Injection.
- Refactored `LLMService` and `OrchestratorAgent` to accept `Settings` via constructor.
- Centralized test configuration using a session-scoped Pytest fixture in `conftest.py`.
- Updated `FastAPI` main application to utilize the unified `Settings` class.
- Explicitly pass API key to `LiteLlm` constructor per Google ADK best practices.

## [0.4.0] - 2026-03-27
### Added
- `OrchestratorAgent` implementation using Google ADK.
- Hybrid Chain-of-Thought (CoT) + Structured Output pattern for intent parsing.
- `OrchestratorResponse` Pydantic schema for routing logic.
- Integration test suite for Orchestrator routing verification.
- Architectural documentation for the Orchestrator Agent.

## [0.3.0] - 2026-03-27
### Added
- Google ADK (Agent Development Kit) core integration.
- Unified `LLMService` for providing ADK models to agents.
- `AgentRole` Enum to eliminate magic strings in model selection.
- Automatic API Key mapping for LiteLLM/ADK (`GEMINI_API_KEY`, `GOOGLE_API_KEY`).
- Structured test suite (Unit & Integration) for LLM layer.
- Comprehensive root-level `.gitignore` for professional repository management.
- Architectural documentation for the LLM layer.

## [0.2.0] - 2026-03-20
### Added
- Complete Docker Compose orchestration for all services.
- Multi-stage production Dockerfiles for all layers.
- Health checks and service dependencies configured.

## [0.1.0] - 2026-03-26
### Added
- Initial monorepo structure (`ai/`, `bot/`, `web/`).
- `docker-compose.yml` for unified local development.
- Integrated MongoDB (8.0) and Qdrant (v1.17.0) with custom silent health checks.
- Unified `.env` and `.env.example` at the root level.
- `MARKA_AI_Technical_Document.md` for AI agentic context.
- Configured "Smart Orchestrator" LLM strategy using `gemini-3-flash` and `gemini-3.1-pro`.
- Basic FastAPI application initialized with `uv` and `fastapi-cli`.
