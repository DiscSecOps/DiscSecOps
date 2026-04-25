# ============================
# 1. BUILDER STAGE
# ============================
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY app ./app

RUN /root/.local/bin/uv sync --frozen --no-dev


# ============================
# 2. RUNTIME STAGE
# ============================
FROM python:3.12-slim AS runtime

RUN useradd -m appuser

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/app ./app
COPY --from=builder /app/pyproject.toml .

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
