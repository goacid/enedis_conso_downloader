# 🧪 Tests - Guide de Démarrage Rapide

## ⚡ Installation ultra-rapide

```bash
# 1. Installer les dépendances de test (depuis testing/)
cd testing
pip install -r requirements-dev.txt

# 2. Lancer les tests
pytest

# 3. Voir le rapport de couverture
pytest --cov=. --cov-report=html
open htmlcov/index.html  # macOS
```

## 📁 Structure créée

```
enedis_conso_downloader/
├── tests/                          # 📂 Dossier des tests
│   ├── __init__.py                # Init package tests
│   ├── conftest.py                # Configuration pytest & fixtures
│   ├── test_utils.py              # Tests fonctions utilitaires
│   ├── test_driver_setup.py       # Tests setup Selenium
│   ├── test_selenium_interactions.py  # Tests interactions web
│   ├── test_security.py           # Tests de sécurité
│   ├── test_check_security.py     # Tests script check_security
│   └── README.md                  # Documentation des tests
├── .github/
│   └── workflows/
│       └── tests.yml              # 🤖 CI/CD GitHub Actions
├── pytest.ini                      # ⚙️ Configuration pytest
├── requirements-dev.txt            # 📦 Dépendances de développement
├── run_tests.sh                    # 🚀 Script Linux/macOS
├── run_tests.bat                   # 🚀 Script Windows
├── CONTRIBUTING.md                 # 📖 Guide de contribution
└── .gitignore                      # 🔒 Exclusions (mise à jour)
```

## 🎯 Commandes essentielles

### Lancer les tests

```bash
# Méthode 1 : Pytest direct
pytest                              # Tous les tests
pytest -v                           # Verbose
pytest --cov=.                      # Avec couverture
pytest tests/test_utils.py          # Un fichier spécifique

# Méthode 2 : Scripts pratiques
./run_tests.sh                      # Linux/macOS - Tous les tests
./run_tests.sh coverage             # Avec rapport HTML
./run_tests.sh security             # Tests de sécurité uniquement
./run_tests.sh fast                 # Tests en parallèle

run_tests.bat                       # Windows - Tous les tests
run_tests.bat coverage              # Avec rapport HTML
```

### Vérifier la qualité du code

```bash
# Formater le code
black .

# Trier les imports
isort .

# Vérifier le style
flake8 .
```

## 📊 Que teste chaque fichier ?

### `test_utils.py` - Fonctions utilitaires ✅
- ✅ Masquage des données sensibles (emails, passwords)
- ✅ Validation des plages de dates
- ✅ Sélection aléatoire de User-Agent
- ✅ Découpage des périodes en sous-périodes

### `test_driver_setup.py` - Configuration Selenium ✅
- ✅ Création du répertoire de téléchargement
- ✅ Mode headless vs visible
- ✅ Taille de fenêtre
- ✅ Mécanismes anti-détection

### `test_selenium_interactions.py` - Interactions web ✅
- ✅ Acceptation des cookies
- ✅ Login étape 1 (email)
- ✅ Login étape 2 (mot de passe)
- ✅ Navigation vers page consommation
- ✅ Basculement vers iframe
- ✅ Sélection mode Heures

### `test_security.py` - Sécurité ✅
- ✅ Credentials depuis variables d'environnement
- ✅ Validation HTTPS obligatoire
- ✅ Masquage dans les logs
- ✅ Permissions des fichiers (Unix)
- ✅ User-Agent réaliste
- ✅ Absence de credentials en dur

### `test_check_security.py` - Script de vérification ✅
- ✅ Vérification permissions fichiers
- ✅ Variables d'environnement
- ✅ Fichier .gitignore
- ✅ Fichier config.py

## 🤖 GitHub Actions

### Configuration automatique

Le fichier `.github/workflows/tests.yml` lance automatiquement les tests sur :

**Quand ?**
- 🔄 Chaque push sur `main` ou `develop`
- 🔄 Chaque Pull Request vers `main` ou `develop`
- 🔄 Manuellement depuis l'onglet Actions

**Où ?**
- 🐧 Ubuntu (Linux)
- 🪟 Windows
- 🍎 macOS

**Avec quoi ?**
- 🐍 Python 3.9, 3.10, 3.11, 3.12

**Résultat** : **12 environnements testés** (3 OS × 4 versions Python)

### Configurer les secrets GitHub (optionnel)

Pour tester avec de vraies credentials :

1. Allez dans **Settings** → **Secrets and variables** → **Actions**
2. Ajoutez :
   - `ACCOUNT_EMAIL` : Votre email Enedis
   - `ACCOUNT_PASSWORD` : Votre mot de passe

⚠️ Si non configurés, les tests utilisent `test@example.com`

## 📈 Couverture de code

### Objectifs

- ✅ **Minimum** : 70%
- ✅ **Cible** : 85%
- ✅ **Excellent** : 95%+

### Voir le rapport

```bash
# Générer le rapport
pytest --cov=. --cov-report=html

# Ouvrir dans le navigateur
open htmlcov/index.html      # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html     # Windows
```

Le rapport montre :
- ✅ Lignes couvertes (en vert)
- ❌ Lignes non couvertes (en rouge)
- ⚠️ Branches partielles (en jaune)

## 🔧 Fixtures disponibles

Dans `tests/conftest.py`, plusieurs fixtures sont prêtes à l'emploi :

```python
def test_exemple(temp_download_dir, mock_driver, sample_config):
    """
    Fixtures disponibles :
    - temp_download_dir : Répertoire temporaire
    - mock_driver : Mock du WebDriver Selenium
    - mock_wait : Mock de WebDriverWait
    - sample_config : Configuration de test
    - set_env_vars : Variables d'environnement configurées
    - mock_selenium_element : Mock d'un élément Selenium
    """
    assert os.path.exists(temp_download_dir)
    assert mock_driver is not None
    assert sample_config['EMAIL'] == 'test@example.com'
```

## 🚀 Workflow de développement

### Avant de commencer

```bash
# 1. Créer une branche
git checkout -b feature/ma-fonctionnalite

# 2. Coder votre fonctionnalité
# ...

# 3. Ajouter des tests
# Créer tests/test_ma_fonctionnalite.py
```

### Avant de committer

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

# 5. Si tout est OK, committer
git add .
git commit -m "feat: Ma nouvelle fonctionnalité"
git push origin feature/ma-fonctionnalite
```

### Créer une Pull Request

1. Ouvrez GitHub
2. Créez la PR
3. Attendez que les tests CI passent ✅
4. Demandez une revue de code

## 📚 Ressources

- [Documentation pytest](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Documentation complète des tests](tests/README.md)
- [Guide de contribution](CONTRIBUTING.md)
- [Configuration GitHub Actions](.github/README.md)

## ❓ FAQ

### Les tests ne trouvent pas le module `conso_downloader`

**Solution** : Assurez-vous d'être dans le bon répertoire
```bash
cd /path/to/enedis_conso_downloader
pytest
```

### ImportError: cannot import name 'xxx'

**Solution** : Installez les dépendances
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Les tests de sécurité échouent sur Windows

**Normal** : Les tests de permissions Unix sont ignorés automatiquement sur Windows (`@pytest.mark.skipif`)

### Comment déboguer un test qui échoue ?

```bash
# Option 1 : Mode verbose
pytest -vv

# Option 2 : Afficher les prints
pytest -s

# Option 3 : S'arrêter au premier échec
pytest -x

# Option 4 : Utiliser pdb
pytest --pdb
```

### Comment ajouter un nouveau test ?

```python
# tests/test_ma_fonctionnalite.py
import pytest

class TestMaFonctionnalite:
    def test_comportement_normal(self):
        # Arrange
        input_value = 42
        
        # Act
        result = ma_fonction(input_value)
        
        # Assert
        assert result == 84
    
    def test_cas_erreur(self):
        with pytest.raises(ValueError):
            ma_fonction(-1)
```

## 🎉 C'est prêt !

Vous avez maintenant une suite de tests complète pour votre projet :

- ✅ Tests unitaires
- ✅ Tests de sécurité
- ✅ Tests d'intégration Selenium
- ✅ CI/CD GitHub Actions
- ✅ Rapports de couverture
- ✅ Scripts de lancement faciles

**Prochaine étape** : Lancez les tests !

```bash
./run_tests.sh coverage
```

Puis ouvrez `htmlcov/index.html` pour voir le rapport 📊

---

**Besoin d'aide ?** Consultez [tests/README.md](tests/README.md) ou [CONTRIBUTING.md](CONTRIBUTING.md)
