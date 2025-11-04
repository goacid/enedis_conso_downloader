#!/bin/bash
# Script pour lancer les tests avec différentes options

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_info() {
    echo -e "${BLUE}ℹ ${NC}$1"
}

print_success() {
    echo -e "${GREEN}✓ ${NC}$1"
}

print_warning() {
    echo -e "${YELLOW}⚠ ${NC}$1"
}

print_error() {
    echo -e "${RED}✗ ${NC}$1"
}

# Fonction d'aide
show_help() {
    cat << EOF
Usage: ./run_tests.sh [OPTIONS]

Options de test :
    all         Lancer tous les tests (défaut)
    unit        Lancer uniquement les tests unitaires
    security    Lancer uniquement les tests de sécurité
    coverage    Lancer les tests avec rapport de couverture HTML
    fast        Lancer les tests en parallèle (rapide)
    verbose     Lancer les tests en mode verbose
    watch       Re-lancer les tests à chaque modification
    
Autres options :
    install     Installer les dépendances de test
    clean       Nettoyer les fichiers de cache et rapports
    help        Afficher cette aide

Exemples :
    ./run_tests.sh                  # Lancer tous les tests
    ./run_tests.sh coverage         # Tests avec couverture
    ./run_tests.sh fast             # Tests en parallèle
    ./run_tests.sh unit             # Tests unitaires uniquement

EOF
}

# Installer les dépendances
install_deps() {
    print_info "Installation des dépendances de test..."
    pip install -r requirements-dev.txt
    print_success "Dépendances installées"
}

# Nettoyer les fichiers
clean_files() {
    print_info "Nettoyage des fichiers de cache et rapports..."
    rm -rf .pytest_cache
    rm -rf htmlcov
    rm -rf .coverage
    rm -rf coverage.xml
    rm -rf *.egg-info
    rm -rf dist
    rm -rf build
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    print_success "Nettoyage terminé"
}

# Vérifier que pytest est installé
check_pytest() {
    if ! command -v pytest &> /dev/null; then
        print_error "pytest n'est pas installé"
        print_info "Installation des dépendances..."
        install_deps
    fi
}

# Configuration des variables d'environnement de test
setup_test_env() {
    export ACCOUNT_EMAIL="${ACCOUNT_EMAIL:-test@example.com}"
    export ACCOUNT_PASSWORD="${ACCOUNT_PASSWORD:-TestPassword123}"
    export BASE_URL="${BASE_URL:-https://mon-compte-particulier.enedis.fr/}"
}

# Tests standard
run_all_tests() {
    print_info "Lancement de tous les tests..."
    setup_test_env
    pytest tests/ -v --rootdir=..
    print_success "Tests terminés"
}

# Tests unitaires uniquement
run_unit_tests() {
    print_info "Lancement des tests unitaires..."
    setup_test_env
    pytest tests/test_utils.py tests/test_driver_setup.py -v
    print_success "Tests unitaires terminés"
}

# Tests de sécurité
run_security_tests() {
    print_info "Lancement des tests de sécurité..."
    setup_test_env
    pytest tests/test_security.py tests/test_check_security.py -v
    print_success "Tests de sécurité terminés"
}

# Tests avec couverture
run_coverage_tests() {
    print_info "Lancement des tests avec couverture..."
    setup_test_env
    pytest tests/ --cov=.. --cov-report=html --cov-report=term-missing --rootdir=..
    print_success "Tests avec couverture terminés"
    print_info "Rapport HTML généré dans htmlcov/index.html"
}

# Tests rapides (parallèles)
run_fast_tests() {
    print_info "Lancement des tests en parallèle..."
    setup_test_env
    pytest tests/ -n auto -v --rootdir=..
    print_success "Tests rapides terminés"
}

# Tests verbose
run_verbose_tests() {
    print_info "Lancement des tests en mode verbose..."
    setup_test_env
    pytest tests/ -vv -s --rootdir=..
    print_success "Tests verbose terminés"
}

# Mode watch (nécessite pytest-watch)
run_watch_tests() {
    print_info "Lancement du mode watch..."
    if ! command -v ptw &> /dev/null; then
        print_warning "pytest-watch n'est pas installé"
        print_info "Installation..."
        pip install pytest-watch
    fi
    setup_test_env
    ptw tests/
}

# Main
main() {
    case "${1:-all}" in
        all)
            check_pytest
            run_all_tests
            ;;
        unit)
            check_pytest
            run_unit_tests
            ;;
        security)
            check_pytest
            run_security_tests
            ;;
        coverage)
            check_pytest
            run_coverage_tests
            ;;
        fast)
            check_pytest
            run_fast_tests
            ;;
        verbose)
            check_pytest
            run_verbose_tests
            ;;
        watch)
            check_pytest
            run_watch_tests
            ;;
        install)
            install_deps
            ;;
        clean)
            clean_files
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Option inconnue: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
