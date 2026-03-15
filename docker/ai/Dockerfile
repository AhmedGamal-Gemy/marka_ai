# ==========================================
# Stage 1: Development
# ==========================================
FROM python:3.12-slim AS development

WORKDIR /app

# Install uv (fast Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies (includes dev dependencies for development)
COPY ai/pyproject.toml ./
RUN uv sync --all-extras

# Copy source code
COPY ai/ .

# Expose port
EXPOSE 8000

# Start development server
CMD ["uv", "run", "fastapi", "dev", "ai/app/main.py"]

# ==========================================
# Stage 2: Production Build
# ==========================================
FROM python:3.12-slim AS production-build

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies (no dev dependencies)
COPY ai/pyproject.toml ./
RUN uv sync --frozen --no-dev

# Copy source code
COPY ai/ .

# Build Python package
RUN uv pip install --no-deps -e .

# ==========================================
# Stage 3: Production Image
# ==========================================
FROM python:3.12-slim AS production

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies (no dev dependencies)
COPY ai/pyproject.toml ./
RUN uv sync --frozen --no-dev

# Copy source code
COPY ai/ .

# Create non-root user for security
RUN addgroup -g 1001 -S python && \
    adduser -S python -u 1001 && \
    chown -R python:python /app

USER python

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').status == 200"

# Start production server
CMD ["uv", "run", "fastapi", "start", "ai/app/main.py", "--host", "0.0.0.0"]
