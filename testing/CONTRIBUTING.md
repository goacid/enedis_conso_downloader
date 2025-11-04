# Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet ! 🎉

## 📋 Table des matières

- [Code de conduite](#code-de-conduite)
- [Comment contribuer](#comment-contribuer)
- [Configuration de l'environnement de développement](#configuration-de-lenvironnement-de-développement)
- [Lancer les tests](#lancer-les-tests)
- [Standards de code](#standards-de-code)
- [Processus de Pull Request](#processus-de-pull-request)

## 🤝 Code de conduite

Ce projet suit un code de conduite standard :
- Respectez les autres contributeurs
- Soyez constructif dans vos critiques
- Concentrez-vous sur le code, pas sur les personnes

## 💡 Comment contribuer

Il y a plusieurs façons de contribuer :

### 🐛 Signaler des bugs

1. Vérifiez que le bug n'a pas déjà été signalé dans les [Issues](https://github.com/goacid/enedis_conso_downloader/issues)
2. Créez une nouvelle issue avec :
   - Un titre clair et descriptif
   - Les étapes pour reproduire le problème
   - Le comportement attendu vs observé
   - Votre environnement (OS, version Python, etc.)
   - Les logs pertinents

### ✨ Proposer des améliorations

1. Créez une issue décrivant l'amélioration
2. Expliquez pourquoi cette amélioration serait utile
3. Attendez les retours avant de commencer à coder

### 🔧 Soumettre des modifications

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 🛠️ Configuration de l'environnement de développement

### 1. Cloner le repository

```bash
git clone https://github.com/goacid/enedis_conso_downloader.git
cd enedis_conso_downloader
```

### 2. Créer un environnement virtuel

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Installer les dépendances de développement

```bash
# Depuis le répertoire testing/
pip install -r requirements-dev.txt
```

### 4. Configurer les credentials de test

```bash
# Option 1 : Variables d'environnement
export ACCOUNT_EMAIL="test@example.com"
export ACCOUNT_PASSWORD="TestPassword123!"

# Option 2 : Fichier .env
cat > .env << EOF
ACCOUNT_EMAIL=test@example.com
ACCOUNT_PASSWORD=TestPassword123!
EOF
chmod 600 .env
```

### 5. Installer les hooks pre-commit (recommandé)

```bash
pip install pre-commit
pre-commit install
```

Cela exécutera automatiquement les vérifications de code avant chaque commit.

## 🧪 Lancer les tests

### Tests de base

```bash
# Tous les tests
pytest

# Tests en mode verbose
pytest -v

# Tests avec couverture
pytest --cov=. --cov-report=html

# Un fichier de test spécifique
pytest tests/test_utils.py

# Une classe de test spécifique
pytest tests/test_utils.py::TestMaskSensitiveData

# Un test spécifique
pytest tests/test_utils.py::TestMaskSensitiveData::test_mask_email
```

### Scripts de test

```bash
# Linux/macOS
./run_tests.sh                  # Tous les tests
./run_tests.sh coverage         # Avec couverture
./run_tests.sh security         # Tests de sécurité
./run_tests.sh fast             # En parallèle
./run_tests.sh verbose          # Mode verbose

# Windows
run_tests.bat                   # Tous les tests
run_tests.bat coverage          # Avec couverture
run_tests.bat security          # Tests de sécurité
```

### Tests par catégorie

```bash
# Tests unitaires uniquement
pytest tests/test_utils.py tests/test_driver_setup.py

# Tests de sécurité uniquement
pytest tests/test_security.py tests/test_check_security.py

# Tests d'intégration Selenium
pytest tests/test_selenium_interactions.py
```

### Vérifier la couverture

```bash
# Générer le rapport HTML
pytest --cov=. --cov-report=html

# Ouvrir le rapport
# Linux
xdg-open htmlcov/index.html
# macOS
open htmlcov/index.html
# Windows
start htmlcov/index.html
```

**Objectif de couverture** : Minimum 70%, idéalement 85%+

## 📐 Standards de code

### Style de code

Ce projet suit les conventions Python standards :

#### PEP 8 avec quelques ajustements

```python
# Longueur de ligne : 127 caractères maximum
# Imports : triés alphabétiquement avec isort
# Formatage : Black

# Bon
def calculate_total(items: List[Item], tax_rate: float = 0.2) -> float:
    """
    Calcule le total avec taxes.
    
    Args:
        items: Liste des items
        tax_rate: Taux de taxe (défaut: 0.2)
    
    Returns:
        Total avec taxes
    """
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)

# Mauvais
def calc(items,tax=0.2):
    return sum([x.price for x in items])*(1+tax)
```

### Vérifications automatiques

Avant de soumettre votre code, exécutez :

```bash
# 1. Formatter avec Black
black .

# 2. Trier les imports avec isort
isort .

# 3. Vérifier avec flake8
flake8 .

# 4. Vérifier les types avec mypy (optionnel)
mypy conso_downloader.py

# 5. Lancer les tests
pytest
```

### Type hints

Utilisez les type hints pour toutes les fonctions publiques :

```python
from typing import Optional, List, Tuple
from datetime import datetime

def validate_date_range(
    start_date: Optional[datetime],
    end_date: Optional[datetime]
) -> Tuple[datetime, datetime]:
    """Valide et normalise les dates."""
    # ...
```

### Documentation

#### Docstrings

Utilisez le format Google pour les docstrings :

```python
def ma_fonction(param1: str, param2: int = 0) -> bool:
    """
    Description courte de la fonction.
    
    Description détaillée si nécessaire, qui peut s'étendre
    sur plusieurs lignes.
    
    Args:
        param1: Description du premier paramètre
        param2: Description du deuxième paramètre (défaut: 0)
    
    Returns:
        Description de la valeur de retour
    
    Raises:
        ValueError: Quand param2 est négatif
    
    Examples:
        >>> ma_fonction("test", 42)
        True
    """
    if param2 < 0:
        raise ValueError("param2 doit être positif")
    return len(param1) > param2
```

#### Commentaires

```python
# Bon : commentaires explicatifs
# Attendre que le captcha soit résolu avant de continuer
WebDriverWait(driver, 30).until(
    lambda d: d.find_element(By.ID, "submit").is_enabled()
)

# Mauvais : commentaires évidents
# Créer une liste
items = []
```

### Sécurité

- ❌ **JAMAIS** de credentials en dur dans le code
- ✅ Toujours utiliser des variables d'environnement ou config
- ✅ Masquer les données sensibles dans les logs
- ✅ Valider toutes les entrées utilisateur
- ✅ Utiliser HTTPS uniquement

```python
# Bon
EMAIL = os.getenv('ACCOUNT_EMAIL')
logger.info(f"Email: {mask_sensitive_data(EMAIL, 'email')}")

# Mauvais
EMAIL = "mon.email@exemple.com"
logger.info(f"Email: {EMAIL}")
```

## 🔄 Processus de Pull Request

### Checklist avant soumission

Avant de soumettre votre PR, vérifiez que :

- [ ] Les tests passent : `pytest`
- [ ] La couverture est maintenue : `pytest --cov`
- [ ] Le code est formaté : `black .`
- [ ] Les imports sont triés : `isort .`
- [ ] Pas d'erreurs de lint : `flake8 .`
- [ ] Pas de credentials en dur
- [ ] Documentation mise à jour si nécessaire
- [ ] Tests ajoutés pour les nouvelles fonctionnalités
- [ ] Le commit est clair et descriptif

### Structure du commit

```bash
# Format recommandé
<type>: <description courte>

<description détaillée optionnelle>

<footer optionnel>

# Types
# feat: Nouvelle fonctionnalité
# fix: Correction de bug
# docs: Documentation uniquement
# style: Formatage, sans changement de code
# refactor: Refactorisation
# test: Ajout/modification de tests
# chore: Maintenance (dépendances, config, etc.)

# Exemples
feat: Ajout support Firefox en plus de Chrome

Permet d'utiliser Firefox comme navigateur alternatif.
Ajout de l'option --browser pour choisir entre chrome et firefox.

Closes #42

---

fix: Correction timeout lors de la résolution du captcha

Le timeout fixe de 20s était trop court dans certains cas.
Passage à une détection dynamique avec is_enabled().

---

test: Ajout tests pour la fonction split_date_range

Couvre tous les cas : périodes courtes, longues, exactes.
Couverture passée de 82% à 91%.
```

### Revue de code

Attendez-vous à :
- Des questions sur vos choix d'implémentation
- Des demandes de modifications
- Des discussions constructives

Soyez patient et ouvert aux retours ! 🙂

### Après la revue

1. Effectuez les modifications demandées
2. Poussez les changements (ils s'ajouteront automatiquement à la PR)
3. Répondez aux commentaires
4. Attendez la validation finale

## 📚 Ressources

- [Documentation Python](https://docs.python.org/3/)
- [PEP 8 – Style Guide](https://peps.python.org/pep-0008/)
- [Type Hints – PEP 484](https://peps.python.org/pep-0484/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)

## 🆘 Besoin d'aide ?

- Consultez la [documentation](README.md)
- Recherchez dans les [issues existantes](https://github.com/goacid/enedis_conso_downloader/issues)
- Créez une nouvelle issue si nécessaire
- Demandez dans les commentaires de votre PR

## 🎉 Remerciements

Merci à tous les contributeurs qui aident à améliorer ce projet !

---

**Note** : Ce guide de contribution peut évoluer. N'hésitez pas à proposer des améliorations !
