@echo off
REM Script pour lancer les tests sous Windows

setlocal

set "TEST_MODE=%1"

if "%TEST_MODE%"=="" set "TEST_MODE=all"

REM Configuration des variables d'environnement de test
if not defined ACCOUNT_EMAIL set "ACCOUNT_EMAIL=test@example.com"
if not defined ACCOUNT_PASSWORD set "ACCOUNT_PASSWORD=TestPassword123"
if not defined BASE_URL set "BASE_URL=https://mon-compte-particulier.enedis.fr/"

REM Vérifier que pytest est installé
where pytest >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] pytest n'est pas installe
    echo [INFO] Installation des dependances...
    pip install -r requirements-dev.txt
)

if "%TEST_MODE%"=="all" (
    echo [INFO] Lancement de tous les tests...
    pytest tests/ -v --rootdir=..
    goto :end
)

if "%TEST_MODE%"=="unit" (
    echo [INFO] Lancement des tests unitaires...
    pytest tests/test_utils.py tests/test_driver_setup.py -v
    goto :end
)

if "%TEST_MODE%"=="security" (
    echo [INFO] Lancement des tests de securite...
    pytest tests/test_security.py tests/test_check_security.py -v
    goto :end
)

if "%TEST_MODE%"=="coverage" (
    echo [INFO] Lancement des tests avec couverture...
    pytest tests/ --cov=.. --cov-report=html --cov-report=term-missing --rootdir=..
    echo [INFO] Rapport HTML genere dans htmlcov/index.html
    goto :end
)

if "%TEST_MODE%"=="fast" (
    echo [INFO] Lancement des tests en parallele...
    pytest tests/ -n auto -v
    goto :end
)

if "%TEST_MODE%"=="verbose" (
    echo [INFO] Lancement des tests en mode verbose...
    pytest tests/ -vv -s
    goto :end
)

if "%TEST_MODE%"=="install" (
    echo [INFO] Installation des dependances...
    pip install -r requirements-dev.txt
    goto :end
)

if "%TEST_MODE%"=="clean" (
    echo [INFO] Nettoyage des fichiers...
    if exist .pytest_cache rmdir /s /q .pytest_cache
    if exist htmlcov rmdir /s /q htmlcov
    if exist .coverage del /q .coverage
    if exist coverage.xml del /q coverage.xml
    for /d /r %%i in (__pycache__) do @if exist "%%i" rmdir /s /q "%%i"
    del /s /q *.pyc >nul 2>&1
    echo [INFO] Nettoyage termine
    goto :end
)

if "%TEST_MODE%"=="help" (
    echo Usage: run_tests.bat [OPTIONS]
    echo.
    echo Options de test :
    echo     all         Lancer tous les tests (defaut)
    echo     unit        Lancer uniquement les tests unitaires
    echo     security    Lancer uniquement les tests de securite
    echo     coverage    Lancer les tests avec rapport de couverture HTML
    echo     fast        Lancer les tests en parallele (rapide)
    echo     verbose     Lancer les tests en mode verbose
    echo.
    echo Autres options :
    echo     install     Installer les dependances de test
    echo     clean       Nettoyer les fichiers de cache et rapports
    echo     help        Afficher cette aide
    echo.
    goto :end
)

echo [ERROR] Option inconnue: %TEST_MODE%
echo Utilisez 'run_tests.bat help' pour voir les options disponibles

:end
endlocal
