# ==========================================
# Stage 1: Development
# ==========================================
FROM python:3.13-slim AS development

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
CMD ["uv", "run", "fastapi", "dev", "app/main.py"]

# ==========================================
# Stage 2: Production Build
# ==========================================
FROM python:3.13-slim AS production-build

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies (no dev dependencies)
COPY ai/pyproject.toml ai/uv.lock ./
RUN uv sync --frozen --no-dev

# Copy source code
COPY ai/ .

# Build Python package
RUN uv pip install --no-deps -e .

# ==========================================
# Stage 3: Production Image
# ==========================================
FROM python:3.13-slim AS production

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy installed deps and source from build stage
COPY --from=production-build /app/.venv ./.venv
COPY --from=production-build /app/app ./app

RUN groupadd --system python && \
    useradd --system --gid python --create-home python && \
    chown -R python:python /app

USER python
EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

