#!/bin/bash
# Script pour lancer les mêmes tests que GitHub Actions localement
# Reproduit exactement le workflow .github/workflows/tests.yml

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Fonctions d'affichage
print_header() {
    echo -e "\n${MAGENTA}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║${NC} ${CYAN}$1${NC}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════════╝${NC}\n"
}

print_step() {
    echo -e "${BLUE}▶${NC} ${CYAN}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Détecter l'OS
detect_os() {
    case "$OSTYPE" in
        linux*)   echo "Linux" ;;
        darwin*)  echo "macOS" ;;
        msys*|cygwin*|win32) echo "Windows" ;;
        *)        echo "Unknown" ;;
    esac
}

OS=$(detect_os)
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')

# Bannière
echo -e "${MAGENTA}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     🧪 GitHub Actions CI - Mode Local                        ║
║                                                               ║
║     Reproduit exactement le workflow GitHub Actions          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}Environnement détecté :${NC}"
echo -e "  • OS       : ${GREEN}$OS${NC}"
echo -e "  • Python   : ${GREEN}$PYTHON_VERSION${NC}"
echo -e "  • Répertoire : ${GREEN}$(pwd)${NC}"
echo ""

# Retourner à la racine du projet
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

print_header "JOB 1/2 : Tests (test)"

# Étape 1 : Vérifier le code (équivalent checkout)
print_step "1. Checkout code"
if [ -d .git ]; then
    print_success "Dépôt Git détecté"
else
    print_warning "Pas de dépôt Git (OK pour test local)"
fi

# Étape 2 : Python déjà configuré
print_step "2. Set up Python"
print_success "Python $PYTHON_VERSION déjà configuré"

# Étape 3 : Installer les dépendances système (optionnel)
print_step "3. Install system dependencies ($OS)"
if [ "$OS" = "Linux" ]; then
    print_warning "Dépendances système (Chrome/ChromeDriver) - à installer manuellement si nécessaire"
    echo "    sudo apt-get install -y chromium-browser chromium-chromedriver"
elif [ "$OS" = "macOS" ]; then
    print_warning "Dépendances système (Chrome/ChromeDriver) - à installer manuellement si nécessaire"
    echo "    brew install --cask chromium && brew install chromedriver"
else
    print_warning "Dépendances système - vérifier Chrome/ChromeDriver installés"
fi

# Étape 4 : Installer les dépendances Python
print_step "4. Install Python dependencies"
echo "    Upgrading pip..."
python3 -m pip install --upgrade pip --quiet

echo "    Installing testing/requirements.txt..."
cd "$PROJECT_ROOT"
pip install -r testing/requirements.txt --quiet

print_success "Dépendances Python installées"

# Étape 5 : Configuration de test
print_step "5. Create test config"
export ACCOUNT_EMAIL="${ACCOUNT_EMAIL:-test@example.com}"
export ACCOUNT_PASSWORD="${ACCOUNT_PASSWORD:-TestPassword123}"
print_success "Variables d'environnement configurées"
echo "    ACCOUNT_EMAIL=$ACCOUNT_EMAIL"
echo "    ACCOUNT_PASSWORD=***"

# Étape 6 : Lancer les tests avec pytest
print_step "6. Run tests with pytest"
cd testing

if pytest tests/ -v --cov=.. --cov-report=xml --cov-report=term; then
    print_success "Tests réussis ✓"
    TEST_RESULT=0
else
    print_error "Tests échoués ✗"
    TEST_RESULT=1
fi

cd "$PROJECT_ROOT"

# Étape 7 : Upload coverage (skip en local)
print_step "7. Upload coverage to Codecov"
print_warning "Skip (mode local) - fichier coverage.xml disponible dans testing/"

# Étape 8 : Vérification de sécurité
if [ "$OS" = "Linux" ] || [ "$OS" = "macOS" ]; then
    print_step "8. Run security checks"
    if python3 check_security.py; then
        print_success "Vérifications de sécurité réussies ✓"
    else
        print_warning "Certaines vérifications de sécurité ont échoué (non bloquant)"
    fi
else
    print_step "8. Run security checks"
    print_warning "Skip (OS Windows)"
fi

echo ""
print_header "JOB 2/2 : Qualité du code (lint)"

# Étape 1 : Installer les outils de lint
print_step "1. Install linting tools"
if ! command -v flake8 &> /dev/null || ! command -v black &> /dev/null || ! command -v isort &> /dev/null; then
    echo "    Installing flake8, black, isort..."
    pip install flake8 black isort --quiet
    print_success "Outils de lint installés"
else
    print_success "Outils de lint déjà installés"
fi

# Étape 2 : Lint avec flake8
print_step "2. Lint with flake8"
echo "    Checking for Python syntax errors..."
if flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=.venv,venv,__pycache__,.git; then
    print_success "Pas d'erreurs de syntaxe Python ✓"
    FLAKE8_ERRORS=0
else
    print_error "Erreurs de syntaxe détectées ✗"
    FLAKE8_ERRORS=1
fi

echo "    Checking for code quality issues (warnings)..."
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=.venv,venv,__pycache__,.git
print_success "Analyse flake8 terminée"

# Étape 3 : Vérifier le formatage avec black
print_step "3. Check code formatting with black"
if black --check --diff . --exclude '/(\.venv|venv|__pycache__|\.git)/' 2>&1 | grep -q "would be reformatted"; then
    print_warning "Code non formaté - exécuter 'black .' pour corriger"
    BLACK_RESULT=1
else
    print_success "Code bien formaté ✓"
    BLACK_RESULT=0
fi

# Étape 4 : Vérifier le tri des imports avec isort
print_step "4. Check import sorting with isort"
if isort --check-only --diff . --skip .venv --skip venv --skip __pycache__ 2>&1 | grep -q "would be reformatted"; then
    print_warning "Imports non triés - exécuter 'isort .' pour corriger"
    ISORT_RESULT=1
else
    print_success "Imports bien triés ✓"
    ISORT_RESULT=0
fi

# Résumé final
echo ""
print_header "RÉSUMÉ"

echo -e "${CYAN}Job 1 - Tests :${NC}"
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "  ${GREEN}✓${NC} Tests pytest       : ${GREEN}PASSED${NC}"
else
    echo -e "  ${RED}✗${NC} Tests pytest       : ${RED}FAILED${NC}"
fi

echo ""
echo -e "${CYAN}Job 2 - Lint :${NC}"
if [ $FLAKE8_ERRORS -eq 0 ]; then
    echo -e "  ${GREEN}✓${NC} Flake8 (erreurs)   : ${GREEN}PASSED${NC}"
else
    echo -e "  ${RED}✗${NC} Flake8 (erreurs)   : ${RED}FAILED${NC}"
fi

if [ $BLACK_RESULT -eq 0 ]; then
    echo -e "  ${GREEN}✓${NC} Black (formatage)  : ${GREEN}PASSED${NC}"
else
    echo -e "  ${YELLOW}⚠${NC} Black (formatage)  : ${YELLOW}WARNING${NC}"
fi

if [ $ISORT_RESULT -eq 0 ]; then
    echo -e "  ${GREEN}✓${NC} Isort (imports)    : ${GREEN}PASSED${NC}"
else
    echo -e "  ${YELLOW}⚠${NC} Isort (imports)    : ${YELLOW}WARNING${NC}"
fi

echo ""

# Code de sortie global
if [ $TEST_RESULT -eq 0 ] && [ $FLAKE8_ERRORS -eq 0 ]; then
    print_success "🎉 Tous les tests critiques sont passés !"
    echo ""
    if [ $BLACK_RESULT -ne 0 ] || [ $ISORT_RESULT -ne 0 ]; then
        print_warning "Des avertissements de formatage existent (non bloquants)"
        echo -e "    Exécutez : ${BLUE}black .${NC} et ${BLUE}isort .${NC} pour corriger"
    fi
    exit 0
else
    print_error "❌ Certains tests ont échoué"
    echo ""
    echo "Consultez les détails ci-dessus pour corriger les problèmes."
    exit 1
fi
