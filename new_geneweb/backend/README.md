# 🧬 GeneWeb Backend

Backend for the modernized **GeneWeb** project, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.  
It exposes REST APIs, applies business logic, and persists genealogy data in a relational database.  

---

## 📦 Requirements

- **Python 3.12+**
- [Poetry](https://python-poetry.org/) (`>=1.8.3`)
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Setup

### Local Environment (without Docker)

1. Clone the repository:

   ```bash
   git clone https://github.com/EpitechPGE45-2025/G-ING-900-PAR-9-1-legacy-11.git
   cd new_geneweb/backend
   ```

2. Install dependencies with Poetry:

   ```bash
   poetry install --no-root
   ```

3. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

4. Run database migrations:

   ```bash
   poetry run alembic upgrade head
   ```

5. Start the backend:

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

6. Visit API docs:

   * Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
   * Redoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Docker Environment

1. Build and start containers:

   ```bash
   docker compose up --build
   ```

2. The following services will be available:

   * Backend → [http://localhost:8000](http://localhost:8000)
   * PostgreSQL → `localhost:5432`

3. Migrations are applied automatically at container startup.
   To run manually inside the backend container:

   ```bash
   docker compose exec backend poetry run alembic upgrade head
   ```

---

## 🧪 Tests & Quality

Run locally with Poetry:

```bash
# Run tests
poetry run pytest --maxfail=1 --disable-warnings -q --cov=app --cov-report=xml

# Code formatting (Black + isort)
poetry run black .
poetry run isort .

# Linting
poetry run flake8 .

# Type checking
poetry run mypy app/
```

---

## ⚙️ Project Structure

```
backend/
├── app/
│   ├── api/              # API routes (FastAPI controllers)
│   ├── services/         # Domain logic & business rules
│   ├── persistence/      # SQLAlchemy models & repository
│   ├── utils/            # Helpers (e.g. IP filter)
│   └── main.py           # Application entrypoint
├── alembic/              # Migrations
├── tests/                # Unit & functional tests
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```
---

## 📖 API Documentation

Once the backend is running, API documentation is auto-generated:

* Swagger UI: `/docs`
* Redoc: `/redoc`

---

## 🤝 Contributing

Please read the [CONTRIBUTING.md](./CONTRIBUTING.md) for details on:

* Branching strategy
* Commit conventions (Conventional Commits)
* Code style rules
* PR review process