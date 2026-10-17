# syntax=docker/dockerfile:1

FROM python:3.14-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.5.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app

RUN python -m pip install --upgrade pip && \
    python -m pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock poetry.toml README.md LICENSE ./
RUN poetry install --only main --no-root --no-ansi

COPY src ./src
RUN poetry install --only main --no-ansi \
    && (.venv/bin/python -m pip uninstall -y pip setuptools wheel || true)

FROM python:3.14-slim AS runtime

# Apply Debian security updates available when the image is built.
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# The runtime does not need pip or setuptools. Removing them also removes pip's
# vendored dependencies, which otherwise show up in image vulnerability scans.
RUN /usr/local/bin/python -m pip uninstall -y pip setuptools wheel || true

ARG VERSION=dev
ARG REVISION=unknown

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_DATABASE_URL="sqlite:////data/app.db"

LABEL org.opencontainers.image.title="python-github-action-example" \
      org.opencontainers.image.description="FastAPI, SQLAlchemy and Alembic example service" \
      org.opencontainers.image.source="https://github.com/donbowman/python-github-action-example" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.revision="${REVISION}"

RUN groupadd --system app && \
    useradd --system --gid app --create-home --home-dir /app app && \
    mkdir -p /data && \
    chown -R app:app /data

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY alembic.ini ./
COPY migrations ./migrations
COPY src ./src

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=3)"]

CMD ["uvicorn", "example_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
