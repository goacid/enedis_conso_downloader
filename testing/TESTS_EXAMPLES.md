# 🎯 Exemple d'exécution des tests

Ce fichier montre des exemples concrets de commandes pour lancer les tests.

## 🚀 Démarrage rapide (3 étapes)

```bash
# 1. Installer les dépendances (depuis testing/)
cd testing
pip install -r requirements-dev.txt

# 2. Lancer tous les tests
pytest

# 3. Voir le rapport de couverture
pytest --cov=. --cov-report=html && open htmlcov/index.html
```

## 📝 Exemples de commandes

### Lancer tous les tests

```bash
# Via pytest
pytest

# Via le script (Linux/macOS)
./run_tests.sh

# Via le script (Windows)
run_tests.bat
```

**Sortie attendue :**
```
========================= test session starts ==========================
platform linux -- Python 3.11.0, pytest-7.4.0, pluggy-1.0.0
collected 68 items

tests/test_utils.py::TestMaskSensitiveData::test_mask_email PASSED  [ 1%]
tests/test_utils.py::TestMaskSensitiveData::test_mask_short_email PASSED [ 2%]
...
========================= 68 passed in 2.34s ===========================
```

### Tests avec couverture

```bash
# Rapport dans le terminal
pytest --cov=.

# Rapport HTML détaillé
pytest --cov=. --cov-report=html

# Ouvrir le rapport
open htmlcov/index.html      # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html     # Windows
```

**Sortie attendue :**
```
----------- coverage: platform linux, python 3.11.0 -----------
Name                      Stmts   Miss  Cover
---------------------------------------------
conso_downloader.py         450     80    82%
check_security.py           120     24    80%
tests/conftest.py            35      0   100%
tests/test_utils.py         120      0   100%
...
---------------------------------------------
TOTAL                       850    120    86%
```

### Tests par fichier

```bash
# Tester les utilitaires uniquement
pytest tests/test_utils.py

# Tester la sécurité uniquement
pytest tests/test_security.py

# Tester une classe spécifique
pytest tests/test_utils.py::TestMaskSensitiveData

# Tester une fonction spécifique
pytest tests/test_utils.py::TestMaskSensitiveData::test_mask_email
```

**Sortie attendue :**
```
tests/test_utils.py::TestMaskSensitiveData::test_mask_email PASSED [100%]

========================= 1 passed in 0.12s ============================
```

### Tests en mode verbose

```bash
# Afficher plus de détails
pytest -v

# Encore plus de détails
pytest -vv

# Afficher les print() dans les tests
pytest -s

# Combinaison
pytest -vv -s
```

**Sortie attendue :**
```
tests/test_utils.py::TestMaskSensitiveData::test_mask_email PASSED
tests/test_utils.py::TestMaskSensitiveData::test_mask_short_email PASSED
tests/test_utils.py::TestMaskSensitiveData::test_mask_password PASSED
...
========================= 68 passed in 2.45s ===========================
```

### Tests par catégorie

```bash
# Tests unitaires
pytest tests/test_utils.py tests/test_driver_setup.py

# Tests de sécurité
pytest tests/test_security.py tests/test_check_security.py

# Tests d'intégration
pytest tests/test_selenium_interactions.py
```

### Tests en parallèle (rapide)

```bash
# Utiliser tous les CPU disponibles
pytest -n auto

# Utiliser 4 workers
pytest -n 4

# Via le script
./run_tests.sh fast
```

**Sortie attendue :**
```
[gw0] [ 25%] PASSED tests/test_utils.py::TestMaskSensitiveData::test_mask_email
[gw1] [ 50%] PASSED tests/test_utils.py::TestMaskSensitiveData::test_mask_password
[gw2] [ 75%] PASSED tests/test_security.py::TestCredentialsValidation::test_https_url_validation
[gw3] [100%] PASSED tests/test_driver_setup.py::TestSetupDriver::test_setup_driver_creates_download_dir

========================= 68 passed in 1.12s ===========================
(2x plus rapide !)
```

### Débogage

```bash
# S'arrêter au premier échec
pytest -x

# Afficher les 10 tests les plus lents
pytest --durations=10

# Mode débogage (pdb)
pytest --pdb

# Ré-exécuter seulement les tests qui ont échoué
pytest --lf

# Ré-exécuter les échecs en premier, puis tous les autres
pytest --ff
```

### Générer des rapports

```bash
# Rapport XML (pour CI/CD)
pytest --junitxml=report.xml

# Rapport HTML
pytest --html=report.html --self-contained-html

# Les deux
pytest --junitxml=report.xml --html=report.html
```

## 🎨 Exemples avec les scripts

### Linux/macOS (run_tests.sh)

```bash
# Aide
./run_tests.sh help

# Tous les tests
./run_tests.sh

# Tests avec couverture HTML
./run_tests.sh coverage

# Tests de sécurité uniquement
./run_tests.sh security

# Tests unitaires uniquement
./run_tests.sh unit

# Tests en parallèle (rapide)
./run_tests.sh fast

# Mode verbose
./run_tests.sh verbose

# Installer les dépendances
./run_tests.sh install

# Nettoyer les fichiers de cache
./run_tests.sh clean
```

### Windows (run_tests.bat)

```batch
REM Aide
run_tests.bat help

REM Tous les tests
run_tests.bat

REM Tests avec couverture HTML
run_tests.bat coverage

REM Tests de sécurité uniquement
run_tests.bat security

REM Nettoyer
run_tests.bat clean
```

## 🔍 Vérifier l'installation

```bash
# Vérifier que tout est installé correctement
./verify_tests_installation.sh
```

**Sortie attendue :**
```
======================================================================
🧪 Vérification de l'installation des tests
======================================================================

📂 Structure des tests :
------------------------
✓ tests/
✓ tests/__init__.py
✓ tests/conftest.py
✓ tests/test_utils.py
✓ tests/test_driver_setup.py
✓ tests/test_selenium_interactions.py
✓ tests/test_security.py
✓ tests/test_check_security.py
✓ tests/README.md

⚙️  Configuration :
-------------------
✓ pytest.ini
✓ requirements-dev.txt
✓ .gitignore

🚀 Scripts de lancement :
-------------------------
✓ run_tests.sh
✓ run_tests.bat

🤖 CI/CD GitHub Actions :
-------------------------
✓ .github/workflows/
✓ .github/workflows/tests.yml
✓ .github/README.md

📖 Documentation :
------------------
✓ CONTRIBUTING.md
✓ TESTS_QUICKSTART.md

======================================================================
🔍 Vérification des dépendances :
======================================================================

✓ pytest installé : pytest 7.4.0
✓ pytest-cov installé
✓ black installé
✓ flake8 installé

======================================================================
🧪 Test rapide :
======================================================================

tests/test_utils.py::TestMaskSensitiveData::test_mask_email PASSED [100%]

✓ Test rapide réussi !

======================================================================
📊 Résumé :
======================================================================

Fichiers créés :
  • 7 fichiers de tests (tests/*.py)
  • 1 configuration pytest (pytest.ini)
  • 1 workflow GitHub Actions (.github/workflows/tests.yml)
  • 2 scripts de lancement (run_tests.sh, run_tests.bat)
  • 4 fichiers de documentation

Prochaines étapes :

  1. Installer les dépendances :
     pip install -r requirements-dev.txt

  2. Lancer tous les tests :
     ./run_tests.sh  (ou pytest)

  3. Voir le rapport de couverture :
     ./run_tests.sh coverage

  4. Consulter la documentation :
     cat TESTS_QUICKSTART.md

======================================================================
```

## 🐛 Exemples de débogage

### Test qui échoue

```bash
# Lancer avec -vv pour voir les détails
pytest tests/test_utils.py::TestMaskSensitiveData::test_mask_email -vv
```

**Si le test échoue :**
```
FAILED tests/test_utils.py::TestMaskSensitiveData::test_mask_email - AssertionError: assert 'john.doe@example.com' == 'jo***@example.com'
  + where 'john.doe@example.com' = mask_sensitive_data('john.doe@example.com', 'email')
```

### Voir les prints dans les tests

```bash
# Utiliser -s pour voir les print()
pytest -s tests/test_utils.py
```

### Mode interactif avec pdb

```bash
# S'arrêter en mode débogage au premier échec
pytest --pdb
```

**Commandes pdb utiles :**
- `l` : voir le code autour
- `p variable` : afficher une variable
- `c` : continuer
- `q` : quitter

## 📊 Rapport de couverture détaillé

```bash
# Générer le rapport HTML
pytest --cov=. --cov-report=html

# Le rapport se trouve dans htmlcov/index.html
```

**Le rapport HTML montre :**
- ✅ Lignes couvertes (en vert)
- ❌ Lignes non couvertes (en rouge)
- ⚠️ Branches partielles (en jaune)
- 📊 Statistiques par fichier
- 🔍 Code source annoté

## 🎯 Workflow de développement

### 1. Avant de coder

```bash
# Créer une branche
git checkout -b feature/ma-fonctionnalite
```

### 2. Pendant le développement

```bash
# Lancer les tests en continu (watch mode)
pytest-watch
# ou
ptw
```

### 3. Avant de committer

```bash
# 1. Formater le code
black .
isort .

# 2. Vérifier le style
flake8 .

# 3. Lancer les tests
pytest

# 4. Vérifier la couverture
pytest --cov=. --cov-report=term-missing

# 5. Si tout est OK
git add .
git commit -m "feat: Ma nouvelle fonctionnalité"
```

### 4. Avant de pousser

```bash
# Lancer tous les tests une dernière fois
./run_tests.sh coverage

# Vérifier le rapport
open htmlcov/index.html

# Pousser
git push origin feature/ma-fonctionnalite
```

## 🤖 GitHub Actions

Une fois poussé, GitHub Actions va automatiquement :

1. ✅ Installer les dépendances
2. ✅ Lancer les tests sur 12 environnements :
   - Ubuntu + Python 3.9, 3.10, 3.11, 3.12
   - Windows + Python 3.9, 3.10, 3.11, 3.12
   - macOS + Python 3.9, 3.10, 3.11, 3.12
3. ✅ Générer le rapport de couverture
4. ✅ Upload vers Codecov
5. ✅ Vérifier la qualité du code (flake8, black, isort)

Vous pouvez suivre l'exécution dans l'onglet **Actions** de votre repo GitHub.

## 📚 Ressources

- [Documentation pytest](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Guide de démarrage rapide](TESTS_QUICKSTART.md)
- [Documentation complète](tests/README.md)
- [Guide de contribution](CONTRIBUTING.md)

---

**✅ Vous êtes prêt à lancer les tests !**

Commencez par :
```bash
pip install -r requirements-dev.txt
pytest
```
