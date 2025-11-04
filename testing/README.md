# 🧪 Testing - Suite de tests complète

Ce répertoire contient **tous les fichiers relatifs aux tests** du projet `enedis_conso_downloader`.

## 📂 Structure

```
testing/
├── tests/                          # 📁 Tests pytest
│   ├── __init__.py                # Init package
│   ├── conftest.py                # Configuration & fixtures
│   ├── test_utils.py              # Tests utilitaires (25 tests)
│   ├── test_driver_setup.py       # Tests Selenium setup (6 tests)
│   ├── test_selenium_interactions.py  # Tests interactions web (15 tests)
│   ├── test_security.py           # Tests sécurité (12 tests)
│   ├── test_check_security.py     # Tests check_security.py (10 tests)
│   └── README.md                  # Documentation détaillée
│
├── pytest.ini                      # ⚙️ Configuration pytest
├── requirements-dev.txt            # 📦 Dépendances de test
│
├── run_tests.sh                    # 🚀 Script Linux/macOS
├── run_tests.bat                   # 🚀 Script Windows
├── verify_tests_installation.sh    # ✅ Vérification installation
│
├── CONTRIBUTING.md                 # 📖 Guide de contribution
├── TESTS_QUICKSTART.md            # 🚀 Démarrage rapide
├── TESTS_SUMMARY.md               # 📊 Récapitulatif
├── TESTS_EXAMPLES.md              # 📝 Exemples d'utilisation
│
└── README.md                       # 📄 Ce fichier
```

## ⚡ Démarrage rapide

### Installation

```bash
# Depuis la racine du projet
cd testing
pip install -r requirements-dev.txt
```

### Lancer les tests

```bash
# Méthode 1 : Via le script (recommandé)
./run_tests.sh                  # Tous les tests
./run_tests.sh coverage         # Avec rapport de couverture
./run_tests.sh security         # Tests de sécurité
./run_tests.sh fast             # En parallèle

# Méthode 2 : Via pytest
pytest                          # Tous les tests
pytest tests/test_utils.py      # Un fichier spécifique
pytest -v --cov=.. --cov-report=html  # Avec couverture
```

### Windows

```batch
cd testing
run_tests.bat                   # Tous les tests
run_tests.bat coverage          # Avec couverture
```

## 📊 Tests disponibles

| Fichier | Tests | Couverture | Description |
|---------|-------|-----------|-------------|
| `test_utils.py` | 25 | ~90% | Fonctions utilitaires (masquage, dates, UA) |
| `test_driver_setup.py` | 6 | ~85% | Configuration Selenium |
| `test_selenium_interactions.py` | 15 | ~75% | Interactions web |
| `test_security.py` | 12 | ~95% | Tests de sécurité |
| `test_check_security.py` | 10 | ~80% | Script check_security |

**Total : 68 tests, ~82% de couverture globale**

## 🎯 Commandes courantes

```bash
# Depuis le répertoire testing/

# Tous les tests
pytest

# Tests avec détails
pytest -v

# Tests avec couverture
pytest --cov=.. --cov-report=html
open htmlcov/index.html  # Ouvrir le rapport

# Tests spécifiques
pytest tests/test_utils.py
pytest tests/test_security.py -v

# Tests en parallèle (rapide)
pytest -n auto

# Mode watch (re-lancer automatiquement)
ptw

# Débogage
pytest -x              # Arrêter au premier échec
pytest --pdb           # Mode débogage interactif
pytest -vv -s          # Très verbose avec prints
```

## 📝 Scripts disponibles

### `run_tests.sh` / `run_tests.bat`

```bash
./run_tests.sh [OPTION]

Options:
  all       - Tous les tests (défaut)
  unit      - Tests unitaires uniquement
  security  - Tests de sécurité uniquement
  coverage  - Tests avec rapport de couverture HTML
  fast      - Tests en parallèle (rapide)
  verbose   - Mode très détaillé
  install   - Installer les dépendances
  clean     - Nettoyer les fichiers de cache
  help      - Afficher l'aide
```

### `verify_tests_installation.sh`

Vérifie que tout est correctement installé et configuré.

```bash
./verify_tests_installation.sh
```

## 📚 Documentation

- **[TESTS_QUICKSTART.md](TESTS_QUICKSTART.md)** - Guide de démarrage rapide
- **[TESTS_EXAMPLES.md](TESTS_EXAMPLES.md)** - Exemples de commandes
- **[TESTS_SUMMARY.md](TESTS_SUMMARY.md)** - Récapitulatif complet
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guide de contribution
- **[tests/README.md](tests/README.md)** - Documentation détaillée des tests

## 🤖 CI/CD GitHub Actions

Les tests sont automatiquement lancés via GitHub Actions sur chaque push/PR.

**Configuration** : `../.github/workflows/tests.yml`

**Environnements testés** :
- Ubuntu, Windows, macOS
- Python 3.9, 3.10, 3.11, 3.12
- **Total : 12 combinaisons**

## 🔧 Configuration

### `pytest.ini`

Configuration principale de pytest :
- Répertoires de tests
- Markers personnalisés
- Options de couverture
- Filtres de warnings

### `requirements-dev.txt`

Dépendances de développement :
- pytest + plugins (cov, mock, timeout, xdist)
- Outils de qualité (black, flake8, isort, mypy)
- Coverage

## 🎯 Objectifs de couverture

- **Minimum** : 70%
- **Cible** : 85%
- **Actuel** : ~82%

## 🐛 Dépannage

### Les tests ne trouvent pas les modules

```bash
# Assurez-vous d'être dans le répertoire testing/
cd testing
pytest
```

### ImportError

```bash
# Installer les dépendances
pip install -r requirements-dev.txt
```

### Tests qui échouent

```bash
# Mode verbose pour voir les détails
pytest -vv

# Avec les prints
pytest -s

# Débogage interactif
pytest --pdb
```

## 🚀 Workflow de développement

### 1. Avant de coder

```bash
cd testing
./run_tests.sh  # Vérifier que tout fonctionne
```

### 2. Après avoir codé

```bash
# Ajouter/modifier des tests
vim tests/test_ma_fonctionnalite.py

# Lancer les tests
pytest tests/test_ma_fonctionnalite.py

# Vérifier la couverture
pytest --cov=.. --cov-report=term-missing
```

### 3. Avant de committer

```bash
# Formater le code (depuis la racine du projet)
cd ..
black .
isort .
flake8 .

# Lancer tous les tests
cd testing
./run_tests.sh coverage

# Si tout est OK
cd ..
git add .
git commit -m "feat: Ma nouvelle fonctionnalité"
```

## 📊 Rapports

### Couverture HTML

```bash
pytest --cov=.. --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Rapport XML (pour CI/CD)

```bash
pytest --cov=.. --cov-report=xml
```

### Rapport JUnit

```bash
pytest --junitxml=report.xml
```

## 🆘 Besoin d'aide ?

1. Consultez [TESTS_QUICKSTART.md](TESTS_QUICKSTART.md)
2. Lisez [TESTS_EXAMPLES.md](TESTS_EXAMPLES.md)
3. Vérifiez [tests/README.md](tests/README.md)
4. Créez une issue sur GitHub

## 🎉 Contribution

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les détails sur :
- Standards de code
- Comment ajouter des tests
- Workflow de contribution
- Revue de code

---

**✅ Tous les fichiers de tests sont isolés dans ce répertoire !**

Pour lancer les tests : `cd testing && ./run_tests.sh`
