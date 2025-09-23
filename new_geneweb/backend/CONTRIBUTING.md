# 🤝 Contributing to GeneWeb Backend

Thanks for considering contributing to the **GeneWeb backend**!  
This document provides guidelines to ensure consistency and maintain quality across the project.  

---

## 🛠 Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/EpitechPGE45-2025/G-ING-900-PAR-9-1-legacy-11.git
   cd new_geneweb/backend
   ```

2. Install dependencies:

   ```bash
   poetry install --no-root
   ```

3. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

4. Apply migrations:

   ```bash
   poetry run alembic upgrade head
   ```

5. Start the backend:

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

---

## 🌱 Branching Strategy

We follow a simple Git branching model:

* `dev`: main development branch.
* `issueID-issue`: new issue.

Branches are merged into `dev` via Pull Requests.

---

## 📝 Commit Convention

We use **[Conventional Commits](https://www.conventionalcommits.org/)**:

```
<type>(scope): short description
```

**Types:**

* `feat`: new feature.
* `fix`: bug fix.
* `chore`: maintenance, infra, tooling (CI, Docker…).
* `docs`: documentation only.
* `style`: formatting (no code change).
* `refactor`: code change without adding features or fixing bugs.
* `test`: tests only.
* `ci`: CI/CD configuration.
* `build`: build system or dependencies.

**Examples:**

* `feat(api): add endpoint to fetch people by surname`
* `fix(db): correct migration script for persons table`
* `ci(backend): add GitHub Actions workflow for tests`

---

## 🎨 Code Style

We enforce consistent formatting and linting:

* **Black** → formatting
* **isort** → import sorting
* **Flake8** → linting
* **Mypy** → type checking

Run before committing:

```bash
poetry run black .
poetry run isort .
poetry run flake8 .
poetry run mypy app/
```

---

## 🧪 Tests

* Unit and functional tests are written with **pytest**.
* All new features and bug fixes must include tests.
* Run tests locally:

  ```bash
  poetry run pytest
  ```

---

## ✅ Pull Requests

* Open PRs against the `dev` branch.
* Ensure CI passes (lint, type-check, tests, Docker build).
* Use a clear PR title (same as commit convention).
* Include a PR description with:

  * Goal / Motivation
  * Summary of changes
  * How to test

---

## 🐳 Docker Workflow (Optional)

You can also run the backend inside Docker:

```bash
docker compose up --build
```

Run tests inside the container:

```bash
docker compose run --rm backend pytest
```

---

## 🗄️ Database Migrations

We use **Alembic** for schema migrations.  
Every time you modify or add a model in `app/persistence/models.py`, you must generate and apply a migration.

### Create a new migration

1. Update your SQLAlchemy models.

2. Generate a migration file:
   ```bash
   poetry run alembic revision --autogenerate -m "describe the change"
   ```

Example:

```bash
poetry run alembic revision --autogenerate -m "add birthdate column to Person"
```

3. Review the generated file under `alembic/versions/`.

   * Alembic may not detect complex changes (e.g., renames).
   * Manually edit the script if necessary.

### Apply migrations

Run migrations locally:

```bash
poetry run alembic upgrade head
```

Or inside Docker:

```bash
docker compose exec backend poetry run alembic upgrade head
```

### Rollback (optional)

To revert the last migration:

```bash
poetry run alembic downgrade -1
```

#### **Rule of thumb:**

* Never edit an existing migration once pushed to `dev`.
* Always create a new one when the schema evolves.

---

## 📖 API Documentation

The backend automatically generates API docs at runtime:

* Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
* Redoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)
