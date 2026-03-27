FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project files first to leverage caching
COPY pyproject.toml uv.lock /app/

# Install dependencies
RUN uv sync --no-install-project

# Copy the application code
COPY . /app

# Run the app using the modern FastAPI CLI
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
