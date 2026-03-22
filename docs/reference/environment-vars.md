---
title: Environment Variables
---

# Environment Variables

Complete reference for all environment variables used in Marka AI.

## Root Configuration

These variables are shared across all services. Configure in the root `.env` file.

| Variable | Description | Required |
|----------|-------------|----------|
| `JWT_SECRET` | Secret key for JWT token signing | Yes |
| `AI_SERVICE_KEY` | Service key for Express → FastAPI communication | Yes |
| `POSTGRES_HOST` | PostgreSQL server hostname | Yes |
| `POSTGRES_PORT` | PostgreSQL server port | Yes |
| `POSTGRES_USER` | PostgreSQL username | Yes |
| `POSTGRES_PASSWORD` | PostgreSQL password | Yes |
| `POSTGRES_DB` | PostgreSQL database name | Yes |
| `REDIS_HOST` | Redis server hostname | Yes |
| `REDIS_PORT` | Redis server port | Yes |
| `OPENAI_API_KEY` | OpenAI API key for LLM operations | Conditional |
| `PINECONE_API_KEY` | Pinecone vector database API key | Conditional |

## Backend (Express)

Location: `backend/.env`

| Variable | Description | Default |
|----------|-------------|---------|
| `NODE_ENV` | Environment (development/production) | development |
| `PORT` | Server port | 3000 |
| `JWT_SECRET` | JWT signing secret | - |
| `POSTGRES_HOST` | Database host | localhost |
| `POSTGRES_PORT` | Database port | 5432 |
| `POSTGRES_USER` | Database user | - |
| `POSTGRES_PASSWORD` | Database password | - |
| `POSTGRES_DB` | Database name | - |
| `REDIS_HOST` | Redis host | localhost |
| `REDIS_PORT` | Redis port | 6379 |
| `AI_SERVICE_KEY` | Service key for AI backend | - |

## Frontend (React/Next.js)

Location: `frontend/.env`

| Variable | Description | Default |
|----------|-------------|---------|
| `NODE_ENV` | Environment | development |
| `NEXT_PUBLIC_API_URL` | Backend API URL | http://localhost:3000/api/v1 |

## AI Backend (FastAPI)

Location: `ai/.env`

| Variable | Description | Required |
|----------|-------------|----------|
| `JWT_SECRET` | JWT validation secret | Yes |
| `AI_SERVICE_KEY` | Service key for authentication | Yes |
| `POSTGRES_HOST` | Database host | Yes |
| `POSTGRES_PORT` | Database port | Yes |
| `POSTGRES_USER` | Database user | Yes |
| `POSTGRES_PASSWORD` | Database password | Yes |
| `POSTGRES_DB` | Database name | Yes |
| `REDIS_HOST` | Redis host | Yes |
| `REDIS_PORT` | Redis port | Yes |
| `PINECONE_API_KEY` | Pinecone vector DB key | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Yes |

## Docker Services

When using Docker Compose, these are set automatically:

```yaml
# docker-compose.yml
services:
  postgres:
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: marka_db

  redis:
    ports:
      - "6380:6379"  # Host:Container
```

## Security Notes

- **Never commit `.env` files** to version control
- Use `.env.example` as a template
- Use strong, unique values for `JWT_SECRET` and `AI_SERVICE_KEY`
- Rotate secrets periodically in production
