#!/bin/bash

# Script pour exécuter les tests localement avec la même configuration que le CI

set -e

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Démarrage des tests backend...${NC}"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Erreur: ce script doit être exécuté depuis le répertoire backend${NC}"
    exit 1
fi

# Vérifier que Poetry est installé
if ! command -v poetry &> /dev/null; then
    echo -e "${RED}❌ Erreur: Poetry n'est pas installé${NC}"
    exit 1
fi

# Installation des dépendances
echo -e "${YELLOW}📦 Installation des dépendances...${NC}"
poetry install --no-root

# Formatage du code
echo -e "${YELLOW}🎨 Vérification du formatage (Black)...${NC}"
poetry run black --check . || {
    echo -e "${RED}❌ Formatage incorrect. Exécutez: poetry run black .${NC}"
    exit 1
}

# Vérification des types
echo -e "${YELLOW}🔍 Vérification des types (mypy)...${NC}"
poetry run mypy app/ || {
    echo -e "${RED}❌ Erreurs de types détectées${NC}"
    exit 1
}

# Configuration des variables d'environnement pour les tests
export APP_ENV=test
export APP_NAME=geneweb
export APP_HOST=localhost
export APP_PORT=8000
export DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/geneweb_test

# Tests
echo -e "${YELLOW}🧪 Exécution des tests...${NC}"
poetry run pytest --maxfail=1 --disable-warnings -v --cov=app --cov-report=xml || {
    echo -e "${RED}❌ Des tests ont échoué${NC}"
    echo ""
    echo -e "${YELLOW}🔧 Vérifications à effectuer pour PostgreSQL :${NC}"
    echo -e "   1. ${YELLOW}PostgreSQL est-il installé ?${NC}"
    echo -e "      sudo apt-get install postgresql postgresql-client"
    echo -e "   2. ${YELLOW}Le service PostgreSQL est-il démarré ?${NC}"
    echo -e "      sudo systemctl start postgresql"
    echo -e "      sudo systemctl enable postgresql"
    echo -e "   3. ${YELLOW}L'utilisateur 'user' existe-t-il ?${NC}"
    echo -e "      sudo -u postgres createuser -s user"
    echo -e "   4. ${YELLOW}Le mot de passe est-il configuré ?${NC}"
    echo -e "      sudo -u postgres psql -c \"ALTER ROLE \\\"user\\\" WITH PASSWORD 'password';\""
    echo -e "   5. ${YELLOW}La base de données 'geneweb_test' existe-t-elle ?${NC}"
    echo -e "      sudo -u postgres createdb geneweb_test -O user"
    echo -e "   6. ${YELLOW}Test de connexion :${NC}"
    echo -e "      PGPASSWORD=password psql -h localhost -U user -d geneweb_test -c \"SELECT 1;\""
    echo ""
    echo -e "${YELLOW}💡 Ou utilisez Docker pour un setup automatique :${NC}"
    echo -e "   docker run -d --name geneweb-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=geneweb_test -p 5432:5432 postgres:15"
    echo ""
    exit 1
}

echo -e "${GREEN}✅ Tous les tests sont passés avec succès!${NC}"
