# FastAPI Project Structure

This project follows FastAPI's standard directory structure.

## Directory Structure

```
ai/
├── __init__.py              # Root package init
├── pyproject.toml           # Project configuration
├── uv.lock                  # Locked dependencies
├── app/                     # Main application package
│   ├── __init__.py          # Makes app a Python package
│   ├── main.py              # FastAPI app instance
│   ├── core/                # Core utilities
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   └── v1/              # API version 1
│   │       ├── __init__.py
│   │       ├── middleware/  # Custom middleware
│   │       │   ├── __init__.py
│   │       │   └── auth.py
│   │       └── routes/      # API endpoints
│   ├── agents/              # AI agent implementations
│   ├── llm/                 # LLM integrations
│   ├── rag/                 # RAG (Retrieval-Augmented Generation)
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
├── tests/                   # Test directory
│   └── test_main.py         # Example tests
└── .env                     # Environment variables
```

## Key Files Explained

### `__init__.py` files
- **Purpose**: Makes directories into Python packages
- **Why needed**: Python requires `__init__.py` to recognize directories as packages
- **Location**: Every directory that should be importable

### `app/main.py`
- **Purpose**: Main FastAPI application instance
- **Entry point**: This is what `uv run fastapi dev app/main.py` runs
- **Contains**: App factory, health check endpoints, basic routing

### `app/api/v1/`
- **Purpose**: API version 1 endpoints
- **Pattern**: RESTful API with versioning for future compatibility

### `app/api/v1/middleware/`
- **Purpose**: Custom middleware for request/response handling
- **Example**: `auth.py` for JWT verification and service key validation

## Running the Server

### Development (with hot reload)
```bash
cd ai
uv run fastapi dev app/main.py
```

### Production
```bash
cd ai
uv run fastapi run app/main.py
```

### With specific port
```bash
uv run fastapi dev app/main.py --port 8000
```

## Import Structure

### Internal imports (within app/)
```python
from app.api.v1.middleware.auth import verify_request
from app.schemas.user import UserCreate
from app.services.auth_service import AuthService
```

### External imports (from other modules)
```python
from fastapi import FastAPI, Depends
```

## Important Notes

1. **No relative imports**: Always use absolute imports (starting with `app.`)
2. **Versioned APIs**: Use versioned directories (`api/v1/`, `api/v2/`)
3. **Package structure**: Each directory needs `__init__.py` to be importable
4. **Main entry point**: Always specify `app/main.py` when running FastAPI

## Environment Variables

Required environment variables (defined in `.env`):
- `JWT_SECRET`: Secret key for JWT token encoding/decoding
- `AI_SERVICE_KEY`: Service key for inter-service authentication
- `POSTGRES_HOST`: PostgreSQL database host
- `POSTGRES_PORT`: PostgreSQL database port
- `POSTGRES_USER`: PostgreSQL database user
- `POSTGRES_PASSWORD`: PostgreSQL database password
- `POSTGRES_DB`: PostgreSQL database name
- `REDIS_HOST`: Redis cache host
- `REDIS_PORT`: Redis cache port
- `PINECONE_API_KEY`: Pinecone vector database API key
- `OPENAI_API_KEY`: OpenAI API key

## Common Issues

### ModuleNotFoundError: No module named 'app'
**Solution**: Make sure `app/__init__.py` exists

### ImportError: cannot import name 'verify_request'
**Solution**: Check the import path is correct
- Wrong: `from app.middleware.auth import verify_request`
- Correct: `from app.api.v1.middleware.auth import verify_request`

### FastAPI not found
**Solution**: Run `uv sync` to install dependencies
