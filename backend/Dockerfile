FROM python:3.14-slim AS uv-base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./


FROM uv-base AS production-builder

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --frozen \
    --no-dev \
    --no-install-project

COPY ./backend .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --frozen \
    --no-dev 

FROM python:3.14-slim AS production

WORKDIR /app

COPY --from=production-builder /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["fastapi", "run", "backend/src/main.py", "--host", "0.0.0.0", "--port", "8000"]



FROM uv-base AS development-builder

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --frozen \
    --no-install-project

COPY ./backend .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --frozen

FROM python:3.14-slim AS development

WORKDIR /app

COPY --from=development-builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

CMD ["fastapi", "dev", "run", "backend/src/main.py", "--host", "0.0.0.0", "--port", "8000"]