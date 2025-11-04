# Tests - Enedis Conso Downloader

## 📋 Vue d'ensemble

Cette suite de tests utilise **pytest** pour valider le bon fonctionnement du téléchargeur de données Enedis.

## 🧪 Structure des tests

```
tests/
├── __init__.py                      # Initialisation du package de tests
├── conftest.py                      # Configuration et fixtures pytest
├── test_utils.py                    # Tests des fonctions utilitaires
├── test_driver_setup.py             # Tests du setup Selenium
├── test_selenium_interactions.py    # Tests des interactions web
├── test_security.py                 # Tests de sécurité
└── test_check_security.py           # Tests du script de vérification
```

## 🚀 Installation des dépendances de test

```bash
# Installer toutes les dépendances de développement
pip install -r requirements-dev.txt
```

## ▶️ Lancer les tests

### Tous les tests
```bash
pytest
```

### Tests avec couverture de code
```bash
pytest --cov=. --cov-report=html
```

### Tests spécifiques
```bash
# Tests utilitaires uniquement
pytest tests/test_utils.py

# Tests de sécurité uniquement
pytest tests/test_security.py -v

# Un test spécifique
pytest tests/test_utils.py::TestMaskSensitiveData::test_mask_email
```

### Tests avec détails
```bash
# Mode verbose
pytest -v

# Afficher les print()
pytest -s

# Arrêter au premier échec
pytest -x

# Mode très détaillé
pytest -vv
```

### Tests par catégorie (markers)
```bash
# Tests unitaires uniquement
pytest -m unit

# Exclure les tests lents
pytest -m "not slow"

# Tests de sécurité uniquement
pytest -m security
```

## 📊 Rapport de couverture

Après avoir lancé les tests avec `--cov-report=html`, ouvrez :
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## 🔧 Configuration

La configuration des tests se trouve dans :
- **pytest.ini** : Configuration principale de pytest
- **tests/conftest.py** : Fixtures et configuration partagée

## 📝 Variables d'environnement pour les tests

Les tests utilisent des credentials de test par défaut. Pour tester avec de vraies credentials :

```bash
export ACCOUNT_EMAIL="votre@email.com"
export ACCOUNT_PASSWORD="VotreMotDePasse"
pytest
```

## 🎯 Objectifs de couverture

- **Minimum** : 70% de couverture de code
- **Cible** : 85% de couverture de code
- **Idéal** : 95%+ de couverture de code

## 🐛 Débogage

### Utiliser pdb pour déboguer
```bash
pytest --pdb  # S'arrête au premier échec
```

### Afficher les warnings
```bash
pytest -W all
```

### Tests parallèles (plus rapide)
```bash
pytest -n auto  # Utilise tous les CPU
pytest -n 4     # Utilise 4 workers
```

## 🔐 Tests de sécurité

Les tests de sécurité vérifient :
- ✅ Pas de credentials en dur dans le code
- ✅ Masquage des données sensibles dans les logs
- ✅ Permissions correctes des fichiers
- ✅ Validation HTTPS uniquement
- ✅ Mécanismes anti-détection

```bash
pytest tests/test_security.py -v
```

## 📦 Tests d'intégration

Les tests d'intégration nécessitent :
- Chrome/Chromium installé
- ChromeDriver dans le PATH
- Credentials Enedis valides (optionnel, pour tests complets)

```bash
pytest -m integration
```

## 🚨 CI/CD avec GitHub Actions

Les tests sont automatiquement lancés sur GitHub Actions à chaque push/PR.

Le workflow teste sur :
- **OS** : Ubuntu, Windows, macOS
- **Python** : 3.9, 3.10, 3.11, 3.12

Voir `.github/workflows/tests.yml` pour la configuration.

## 📈 Améliorer les tests

### Ajouter un nouveau test

1. Créer un fichier `test_*.py` dans `tests/`
2. Créer une classe `Test*`
3. Ajouter des méthodes `test_*`

Exemple :
```python
# tests/test_nouvelle_fonctionnalite.py
import pytest

class TestNouvelleFonctionnalite:
    def test_comportement_attendu(self):
        # Arrange
        valeur = 42
        
        # Act
        resultat = ma_fonction(valeur)
        
        # Assert
        assert resultat == 84
```

### Utiliser les fixtures

```python
def test_avec_fixture(temp_download_dir, mock_driver):
    # temp_download_dir et mock_driver sont des fixtures
    # définies dans conftest.py
    assert os.path.exists(temp_download_dir)
    assert mock_driver is not None
```

## 🔍 Commandes utiles

```bash
# Liste tous les tests disponibles
pytest --collect-only

# Ré-exécuter seulement les tests qui ont échoué
pytest --lf

# Ré-exécuter les échecs en premier
pytest --ff

# Voir les tests les plus lents
pytest --durations=10

# Générer un rapport JUnit XML (pour CI)
pytest --junitxml=report.xml

# Générer un rapport HTML
pytest --html=report.html --self-contained-html
```

## 🤝 Contribution

Avant de soumettre un PR :

1. ✅ Tous les tests passent : `pytest`
2. ✅ Couverture > 80% : `pytest --cov`
3. ✅ Code formaté : `black .`
4. ✅ Imports triés : `isort .`
5. ✅ Lint OK : `flake8 .`

## 📚 Ressources

- [Documentation pytest](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [pytest-mock](https://pytest-mock.readthedocs.io/)
