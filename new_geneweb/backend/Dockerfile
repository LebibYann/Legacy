FROM python:3.13-slim

ENV POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry install --only main --no-root

COPY app ./app

COPY wait-db.sh ./wait-db.sh
COPY entrypoint.sh ./entrypoint.sh
RUN echo "" > .env

EXPOSE 8000

ENTRYPOINT ["bash", "entrypoint.sh"]