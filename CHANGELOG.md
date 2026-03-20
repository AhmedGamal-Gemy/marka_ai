# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Complete Docker Compose setup for one-command deployment
- Windows/WSL2 documentation for Docker Desktop on Windows
- WSL2 installation and usage instructions
- One-command docker compose up from WSL2
- All services (Express, FastAPI, React, PostgreSQL, Redis) containerized
- Multi-stage Dockerfiles for production builds
- Health checks for all services
- Environment variable configuration with .env file
- .dockerignore for faster builds
- Service port mappings table documenting host vs container ports
- Docker network configuration for inter-service communication

### Changed
- Node.js updated to version 22 (latest LTS)
- Python updated to version 3.13
- PostgreSQL updated to version 17
- Redis updated to version 8
- Removed obsolete docker-compose version field
- Fixed healthcheck commands for proper shell execution
- Updated CI/CD workflow to use Node 22 (was 20) and Python 3.13 (was 3.12)
- Docker build context paths in CI/CD (now uses root context with file parameter)
- Port mappings: Frontend uses host:5173→container:3000, AI Backend uses host:8001→container:8000, Redis uses host:6380→container:6379

### Fixed
- npm ci replaced with npm install (no lockfiles required)
- AI Dockerfile FastAPI command path fixed (app/main.py instead of ai/app/main.py)
- Service-to-service communication configured with AI_SERVICE_KEY and JWT_SECRET

---

## [0.1.0] - 2026-03-15

### Added
- Project foundation with architecture defined in AGENTS.md
- Three-phase development plan (Validation, MVP, Pilot, Scale)
- Feature tracking system with status symbols
- Quick start guides for each service (Express, FastAPI, React)
- Environment configuration templates for all services
- Zensical documentation setup
- Project structure with backend, ai, frontend folders
- Scrapling integration planning for competitor monitoring

### Changed
- None yet

### Deprecated
- None yet

### Removed
- None yet

### Fixed
- None yet

### Security
- None yet

---

## [0.1.0] - 2026-03-15

### Added
- Initial project structure
- AGENTS.md with architecture rules and coding guidelines
- README.md with quick start and project overview
- plan.md with detailed development roadmap
- feature_log.md with feature tracking and phase planning
- Three-phase roadmap (Validation → MVP → Pilot → Scale)
- Environment configuration templates
- Gitignore configuration
- Zensical documentation setup
- Scrapling integration planning

---

## Future Versions

### [0.2.0] - Planned
- Customer discovery interviews (Phase 1)
- Express API gateway implementation
- FastAPI AI backend setup
- PostgreSQL schema creation
- Redis integration
- React frontend scaffold

### [0.3.0] - Planned
- AI Content Generation Agent (v1)
- Campaign management features
- Multi-platform publishing (Facebook, Instagram)
- RAG pipeline with Pinecone
- Basic analytics dashboard

### [0.4.0] - Planned
- Arabic chatbot v1
- Publishing Agent (full automation)
- Zensical docs live on site
