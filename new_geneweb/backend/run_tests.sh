#!/bin/bash

# Script to run tests locally with the same configuration as CI

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Starting backend tests...${NC}"

# Check that we are in the correct directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Error: this script must be run from the backend directory${NC}"
    exit 1
fi

# Check that Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo -e "${RED}❌ Error: Poetry is not installed${NC}"
    exit 1
fi

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
poetry install --no-root

# Linting
echo -e "${YELLOW}🔍 Linting (ruff)...${NC}"
poetry run ruff check . || {
    echo -e "${RED}❌ Linting errors detected${NC}"
    exit 1
}

# Code formatting
echo -e "${YELLOW}🎨 Checking formatting (Black)...${NC}"
poetry run black --check . || {
    echo -e "${RED}❌ Incorrect formatting. Run: poetry run black .${NC}"
    exit 1
}

# Type checking
echo -e "${YELLOW}🔍 Type checking (mypy)...${NC}"
poetry run mypy app/ || {
    echo -e "${RED}❌ Type errors detected${NC}"
    exit 1
}

# Configure environment variables for tests
export APP_ENV=test
export APP_NAME=geneweb
export APP_HOST=localhost
export APP_PORT=8000
export DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/geneweb_test

# Tests
echo -e "${YELLOW}🧪 Running tests...${NC}"
poetry run pytest --maxfail=1 --disable-warnings -v --cov=app --cov-report=xml || {
    echo -e "${RED}❌ Some tests failed${NC}"
    echo ""
    echo -e "${YELLOW}🔧 PostgreSQL troubleshooting checklist:${NC}"
    echo -e "   1. ${YELLOW}Is PostgreSQL installed?${NC}"
    echo -e "      sudo apt-get install postgresql postgresql-client"
    echo -e "   2. ${YELLOW}Is PostgreSQL service running?${NC}"
    echo -e "      sudo systemctl start postgresql"
    echo -e "      sudo systemctl enable postgresql"
    echo -e "   3. ${YELLOW}Does the 'user' user exist?${NC}"
    echo -e "      sudo -u postgres createuser -s user"
    echo -e "   4. ${YELLOW}Is the password configured?${NC}"
    echo -e "      sudo -u postgres psql -c \"ALTER ROLE \\\"user\\\" WITH PASSWORD 'password';\""
    echo -e "   5. ${YELLOW}Does the 'geneweb_test' database exist?${NC}"
    echo -e "      sudo -u postgres createdb geneweb_test -O user"
    echo -e "   6. ${YELLOW}Connection test:${NC}"
    echo -e "      PGPASSWORD=password psql -h localhost -U user -d geneweb_test -c \"SELECT 1;\""
    echo ""
    echo -e "${YELLOW}💡 Or use Docker for automatic setup:${NC}"
    echo -e "   docker run -d --name geneweb-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=geneweb_test -p 5432:5432 postgres:15"
    echo ""
    exit 1
}

echo -e "${GREEN}✅ All tests passed successfully!${NC}"
