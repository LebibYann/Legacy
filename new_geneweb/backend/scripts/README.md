# 🛠️ GeneWeb Database Scripts

This directory contains Python scripts for managing the GeneWeb database using SQLAlchemy models.

## 📋 Available Scripts

### 1. `setup_database.py`
**Purpose**: Initialize the database by creating all tables

**Usage**:
```bash
# Create all tables (keeping existing data)
poetry run python scripts/setup_database.py

# Drop all tables and recreate (DESTRUCTIVE!)
poetry run python scripts/setup_database.py --drop-all
```

**What it does**:
- ✅ Tests database connection
- ✅ Creates all tables defined in SQLAlchemy models
- ✅ Lists created tables
- ⚠️ Optional: Can drop existing tables first

---

### 2. `delete_database.py`
**Purpose**: Remove all database tables (DESTRUCTIVE)

**Usage**:
```bash
# Drop all tables (with confirmation prompts)
poetry run python scripts/delete_database.py
```

**What it does**:
- ⚠️ Lists all existing tables
- ⚠️ Asks for double confirmation
- 🗑️ Drops all tables and deletes all data
- ✅ Verifies tables are removed

**Safety features**:
- Two confirmation prompts
- Lists tables before deletion
- Requires typing 'DELETE' to confirm

---

### 3. `load_test_data.py`
**Purpose**: Load sample genealogical data for testing

**Usage**:
```bash
# Load test data
poetry run python scripts/load_test_data.py
```

**What it creates**:
- 1 test database ("test_family")
- 6 individuals (grandparents, parents, 2 children)
- 2 families with parent-child relationships
- 2 marriage events

---

## 🚀 Quick Start Workflow

### Initial Setup
```bash
# 1. Create all tables
poetry run python scripts/setup_database.py

# 2. Load test data
poetry run python scripts/load_test_data.py

# 3. Start the API
poetry run uvicorn app.main:app --reload
```

### Reset Database
```bash
# 1. Drop all tables
poetry run python scripts/delete_database.py

# 2. Recreate tables
poetry run python scripts/setup_database.py

# 3. Load fresh test data
poetry run python scripts/load_test_data.py
```

### Quick Reset (Alternative)
```bash
# Drop and recreate in one command
poetry run python scripts/setup_database.py --drop-all

# Then load test data
poetry run python scripts/load_test_data.py
```

---

## 🔧 Requirements

These scripts require:
- Python 3.13+
- Poetry dependencies installed (`poetry install`)
- Valid `.env` file with `DATABASE_URL`
- PostgreSQL server running

---

## 🆚 Scripts vs Alembic Migrations

### Use These Scripts For:
- ✅ **Development**: Quick database setup/reset
- ✅ **Testing**: Clean slate for tests
- ✅ **Prototyping**: Rapid iteration

### Use Alembic For:
- ✅ **Production**: Safe schema changes
- ✅ **Versioning**: Track schema history
- ✅ **Team work**: Share schema changes
- ✅ **Upgrades/Downgrades**: Rollback capability

### Typical Workflow:
```bash
# Development (iterate quickly)
poetry run python scripts/setup_database.py --drop-all
poetry run python scripts/load_test_data.py

# When schema is stable, create migration
poetry run alembic revision --autogenerate -m "Initial schema"

# Apply migration
poetry run alembic upgrade head
```

---

## ⚠️ Important Notes

1. **These scripts bypass Alembic**: They create tables directly from SQLAlchemy models
2. **No migration history**: Alembic won't track changes made by these scripts
3. **Development only**: Use Alembic migrations for production deployments
4. **Data loss**: `delete_database.py` and `--drop-all` delete ALL data

---

## 💡 Tips

### Check Table Status
```bash
# List all tables
# Replace user/password/dbname with values from your .env file
PGPASSWORD=password psql -h localhost -U user -d dbname -c "\dt"

# Count rows in each table
PGPASSWORD=password psql -h localhost -U user -d dbname -c "
  SELECT schemaname, tablename, 
         (xpath('/row/c/text()', query_to_xml('SELECT count(*) as c FROM ' || schemaname || '.' || tablename, false, true, '')))[1]::text::int as count
  FROM pg_tables 
  WHERE schemaname = 'public' 
  ORDER BY tablename;
"
```

### Verify Setup
```bash
# After setup, verify connection
python -c "from app.persistence.db import engine; import asyncio; asyncio.run(engine.dispose())" && echo "✅ Connection OK"

# Check if tables exist
# Replace user/password/dbname with values from your .env file
PGPASSWORD=password psql -h localhost -U user -d dbname -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
```

---

## 📝 Related Files

- `../app/persistence/models.py` - SQLAlchemy model definitions
- `../app/settings.py` - Database configuration
- `../alembic/` - Migration files (for production)
- `../../database_schemas/` - SQL schema documentation (reference only)
