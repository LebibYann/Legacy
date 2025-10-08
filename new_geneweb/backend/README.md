# 🧬 GeneWeb Backend

Backend for the modernized **GeneWeb** project, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.
It exposes REST APIs, applies business logic, and persists genealogy data in a relational database.

---

## 📦 Requirements

- **Python 3.13.x**
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

   **Important environment variables:**
   - `DATABASE_URL` - PostgreSQL connection string
   - `DATABASE_ECHO` - Set to `true` to log all SQL queries (useful for debugging)
   - `ALLOWED_IPS` - IP whitelist for API access

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
# Show coverage report
poetry run coverage report

# Linting + autofixing
poetry run ruff check --fix .

# Code formatting (Black)
poetry run black .

# Type checking
poetry run mypy app/
```

---

## 🗄️ Database Management

### Quick Start

```bash
# Setup database with sample data
poetry run python scripts/setup_database.py
poetry run python scripts/load_test_data.py

# Reset database
poetry run python scripts/teardown_database.py
poetry run python scripts/setup_database.py --drop-all
```

### Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/setup_database.py` | Create all tables | `poetry run python scripts/setup_database.py` |
| `scripts/teardown_database.py` | Drop all tables | `poetry run python scripts/teardown_database.py` |
| `scripts/load_test_data.py` | Load sample data | `poetry run python scripts/load_test_data.py` |

**See** [`scripts/README.md`](scripts/README.md) for detailed documentation.

### Production Migrations

For production deployments, use Alembic:

```bash
# Generate migration
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations
poetry run alembic upgrade head

# Rollback
poetry run alembic downgrade -1
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
├── scripts/              # Database management scripts ✨ NEW
│   ├── setup_database.py
│   ├── teardown_database.py
│   └── load_test_data.py
├── alembic/              # Production migrations
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
