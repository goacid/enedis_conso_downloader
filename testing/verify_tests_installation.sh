#!/bin/bash
# Script de vérification de l'installation des tests

echo "======================================================================"
echo "🧪 Vérification de l'installation des tests"
echo "======================================================================"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        return 0
    else
        echo -e "${RED}✗${NC} $1/"
        return 1
    fi
}

echo "📂 Structure des tests :"
echo "------------------------"
check_dir "tests"
check_file "tests/__init__.py"
check_file "tests/conftest.py"
check_file "tests/test_utils.py"
check_file "tests/test_driver_setup.py"
check_file "tests/test_selenium_interactions.py"
check_file "tests/test_security.py"
check_file "tests/test_check_security.py"
check_file "tests/README.md"
echo ""

echo "⚙️  Configuration :"
echo "-------------------"
check_file "pytest.ini"
check_file "requirements-dev.txt"
check_file ".gitignore"
echo ""

echo "🚀 Scripts de lancement :"
echo "-------------------------"
check_file "run_tests.sh"
check_file "run_tests.bat"
echo ""

echo "🤖 CI/CD GitHub Actions :"
echo "-------------------------"
check_dir ".github/workflows"
check_file ".github/workflows/tests.yml"
check_file ".github/README.md"
echo ""

echo "📖 Documentation :"
echo "------------------"
check_file "CONTRIBUTING.md"
check_file "TESTS_QUICKSTART.md"
echo ""

echo "======================================================================"
echo "🔍 Vérification des dépendances :"
echo "======================================================================"
echo ""

# Vérifier pytest
if command -v pytest &> /dev/null; then
    VERSION=$(pytest --version | head -n 1)
    echo -e "${GREEN}✓${NC} pytest installé : $VERSION"
else
    echo -e "${RED}✗${NC} pytest non installé"
    echo -e "${YELLOW}→${NC} Installer avec : pip install -r requirements-dev.txt"
fi

# Vérifier coverage
if python -c "import pytest_cov" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} pytest-cov installé"
else
    echo -e "${RED}✗${NC} pytest-cov non installé"
fi

# Vérifier black
if command -v black &> /dev/null; then
    echo -e "${GREEN}✓${NC} black installé"
else
    echo -e "${YELLOW}⚠${NC} black non installé (optionnel)"
fi

# Vérifier flake8
if command -v flake8 &> /dev/null; then
    echo -e "${GREEN}✓${NC} flake8 installé"
else
    echo -e "${YELLOW}⚠${NC} flake8 non installé (optionnel)"
fi

echo ""
echo "======================================================================"
echo "🧪 Test rapide :"
echo "======================================================================"
echo ""

# Définir les variables d'environnement pour le test
export ACCOUNT_EMAIL="test@example.com"
export ACCOUNT_PASSWORD="TestPassword123"

# Tenter de lancer pytest
if command -v pytest &> /dev/null; then
    echo -e "${BLUE}ℹ${NC} Lancement d'un test rapide..."
    if pytest tests/test_utils.py::TestMaskSensitiveData::test_mask_email -v; then
        echo ""
        echo -e "${GREEN}✓${NC} Test rapide réussi !"
    else
        echo ""
        echo -e "${RED}✗${NC} Test rapide échoué"
    fi
else
    echo -e "${YELLOW}⚠${NC} Impossible de lancer les tests (pytest non installé)"
fi

echo ""
echo "======================================================================"
echo "📊 Résumé :"
echo "======================================================================"
echo ""
echo "Fichiers créés :"
echo "  • 7 fichiers de tests (tests/*.py)"
echo "  • 1 configuration pytest (pytest.ini)"
echo "  • 1 workflow GitHub Actions (.github/workflows/tests.yml)"
echo "  • 2 scripts de lancement (run_tests.sh, run_tests.bat)"
echo "  • 4 fichiers de documentation"
echo ""
echo "Prochaines étapes :"
echo ""
echo "  1. Installer les dépendances :"
echo "     ${BLUE}pip install -r requirements-dev.txt${NC}"
echo ""
echo "  2. Lancer tous les tests :"
echo "     ${BLUE}./run_tests.sh${NC}  (ou ${BLUE}pytest${NC})"
echo ""
echo "  3. Voir le rapport de couverture :"
echo "     ${BLUE}./run_tests.sh coverage${NC}"
echo ""
echo "  4. Consulter la documentation :"
echo "     ${BLUE}cat TESTS_QUICKSTART.md${NC}"
echo ""
echo "======================================================================"
