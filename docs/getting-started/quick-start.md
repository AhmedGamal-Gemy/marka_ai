---
title: Quick Start
---

# Quick Start

Get Marka AI running on your local machine in minutes.

## Prerequisites

- **Node.js** >= 22
- **Python** >= 3.13
- **Docker** & Docker Compose
- **uv** (Python package manager)

## Option 1: Docker Compose (Recommended)

The fastest way to run all services together.

### Linux / macOS / WSL2

```bash
docker compose up -d
```

### Windows (Docker Desktop)

**IMPORTANT**: On Windows, always run Docker Compose from WSL2.

```powershell
# Open WSL2 and navigate to project
wsl
cd /mnt/d/AHMED_DATA/Projects/marka_ai
docker compose up -d
```

Or from PowerShell in one command:

```powershell
wsl -d Ubuntu -- cd /mnt/d/AHMED_DATA/Projects/marka_ai && docker compose up -d
```

### Services Started

| Service | URL |
|---------|-----|
| Frontend (React) | http://localhost:5173 |
| Backend API (Express) | http://localhost:3000 |
| AI Backend (FastAPI) | http://localhost:8001 |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6380 |

## Option 2: Individual Services

Run services individually for development.

### 1. Environment Setup

```bash
# Copy root .env.example to .env and configure values
cp .env.example .env

# Also copy service-specific env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
cp ai/.env.example ai/.env
```

### 2. Backend (Express)

```bash
cd backend
npm install
npm run dev          # runs on :3000
```

### 3. Frontend (React)

```bash
cd frontend
npm install
npm run dev          # runs on :5173
```

### 4. AI Backend (FastAPI)

```bash
cd ai
uv sync
uv run fastapi dev   # runs on :8000
```

## Verify Installation

Once running, verify services:

1. **Frontend**: Open http://localhost:5173
2. **Backend API**: Visit http://localhost:3000/api/v1/health
3. **AI Backend**: Visit http://localhost:8001/docs (internal only)

## Common Commands

```bash
# Docker
docker compose up -d       # Start all services
docker compose ps          # Check service status
docker compose logs -f     # View logs
docker compose down        # Stop all services

# Backend
cd backend && npm run dev

# Frontend  
cd frontend && npm run dev

# AI Backend
cd ai && uv run fastapi dev
```

## Next Steps

- [Architecture Overview](../architecture/overview.md) - Understand the system design
- [Environment Variables](../reference/environment-vars.md) - Configure your setup

## Troubleshooting

### Port Already in Use

If you get port conflicts, stop other services or modify ports in `docker-compose.yml`.

### Database Connection Issues

Ensure PostgreSQL is running:
```bash
docker compose up -d postgres redis
```

### WSL2 Issues on Windows

If Docker doesn't work from PowerShell, install WSL2:
```powershell
wsl --install
```
