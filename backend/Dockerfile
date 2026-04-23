# ============================
# 1. BUILDER STAGE
# ============================
FROM python:3.12-slim AS builder
 
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*
 
# Install uv (package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
 
WORKDIR /app
 
# Copy project files
COPY pyproject.toml uv.lock ./
COPY app ./app
 
# Install dependencies into a clean directory
RUN /root/.local/bin/uv sync --frozen --no-dev
 
 
# ============================
# 2. RUNTIME STAGE
# ============================
FROM python:3.12-slim AS runtime
 
# Create non-root user
RUN useradd -m appuser
 
WORKDIR /app
 
# Copy environment (dependencies only)
COPY --from=builder /app/.venv ./.venv
 
# Copy application code
COPY app ./app
COPY pyproject.toml .
 
# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH"
 
# Switch to non-root user
USER appuser
 
# Expose API port
EXPOSE 8000
 
# Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]