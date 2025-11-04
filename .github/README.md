# Configuration GitHub Actions pour les Tests

## 📋 Vue d'ensemble

Ce projet utilise **GitHub Actions** pour exécuter automatiquement les tests sur chaque push et pull request.

## 🔧 Configuration

Le workflow est défini dans `.github/workflows/tests.yml` et comprend deux jobs :

### 1. Job `test` - Tests multi-plateforme

Exécute la suite complète de tests sur :
- **Systèmes d'exploitation** : Ubuntu, Windows, macOS
- **Versions Python** : 3.9, 3.10, 3.11, 3.12

**Étapes** :
1. ✅ Checkout du code
2. ✅ Installation de Python
3. ✅ Installation des dépendances système (Chrome/ChromeDriver)
4. ✅ Installation des dépendances Python
5. ✅ Configuration des variables d'environnement de test
6. ✅ Exécution des tests avec pytest
7. ✅ Upload du rapport de couverture vers Codecov
8. ✅ Vérification de sécurité (Linux uniquement)

### 2. Job `lint` - Qualité du code

Vérifie la qualité du code avec :
- **flake8** : Détection d'erreurs de syntaxe et problèmes de style
- **black** : Vérification du formatage du code
- **isort** : Vérification du tri des imports

## 🔐 Secrets GitHub

Pour tester avec de vraies credentials Enedis, configurez ces secrets dans votre repo GitHub :

1. Allez dans **Settings** → **Secrets and variables** → **Actions**
2. Ajoutez ces secrets :
   - `ACCOUNT_EMAIL` : Votre email Enedis
   - `ACCOUNT_PASSWORD` : Votre mot de passe Enedis

⚠️ **Note** : Si ces secrets ne sont pas définis, les tests utiliseront des credentials de test factices (`test@example.com`).

## 🚀 Déclenchement des workflows

Les workflows sont déclenchés automatiquement sur :
- ✅ Push vers `main` ou `develop`
- ✅ Pull Request vers `main` ou `develop`
- ✅ Déclenchement manuel (workflow_dispatch)

### Déclencher manuellement

1. Allez dans l'onglet **Actions** de votre repo
2. Sélectionnez le workflow **Tests**
3. Cliquez sur **Run workflow**
4. Choisissez la branche
5. Cliquez sur **Run workflow**

## 📊 Badges de statut

Ajoutez ces badges à votre README :

```markdown
[![Tests](https://github.com/VOTRE_USERNAME/enedis_conso_downloader/workflows/Tests/badge.svg)](https://github.com/VOTRE_USERNAME/enedis_conso_downloader/actions)
[![codecov](https://codecov.io/gh/VOTRE_USERNAME/enedis_conso_downloader/branch/main/graph/badge.svg)](https://codecov.io/gh/VOTRE_USERNAME/enedis_conso_downloader)
```

Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur GitHub.

## 🔄 Configuration Codecov

Pour activer l'upload de la couverture vers Codecov :

1. Allez sur [codecov.io](https://codecov.io)
2. Connectez-vous avec votre compte GitHub
3. Activez votre repo `enedis_conso_downloader`
4. Le token est automatiquement configuré pour les repos publics

Pour les repos privés, ajoutez le secret :
- `CODECOV_TOKEN` : Token fourni par Codecov

## 📝 Personnalisation

### Modifier les versions Python testées

Dans `.github/workflows/tests.yml`, modifiez la matrice :

```yaml
matrix:
  python-version: ['3.9', '3.10', '3.11', '3.12']
```

### Modifier les systèmes d'exploitation

```yaml
matrix:
  os: [ubuntu-latest, windows-latest, macos-latest]
```

### Ajouter des étapes supplémentaires

Ajoutez de nouvelles étapes dans le fichier YAML :

```yaml
- name: Ma nouvelle étape
  run: |
    echo "Commandes à exécuter"
```

### Configurer les notifications

Ajoutez des notifications Slack, email, etc. :

```yaml
- name: Notification Slack
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 🐛 Dépannage

### Les tests échouent uniquement sur GitHub Actions

**Causes possibles** :
1. Différences d'environnement (paths, permissions, etc.)
2. ChromeDriver non compatible avec la version de Chrome
3. Timeouts trop courts pour l'environnement CI

**Solutions** :
- Vérifiez les logs GitHub Actions
- Ajoutez des `sleep()` supplémentaires si nécessaire
- Augmentez les timeouts pour les environnements CI

### Upload Codecov échoue

**Solution** :
- Vérifiez que le repo est activé sur codecov.io
- Pour les repos privés, ajoutez le secret `CODECOV_TOKEN`
- L'option `fail_ci_if_error: false` empêche l'échec du workflow

### Tests lents sur Windows/macOS

C'est normal, ces environnements sont plus lents sur GitHub Actions.

**Solution** :
- Utilisez `pytest -n auto` pour paralléliser
- Réduisez le nombre de versions Python testées sur ces OS

## 📈 Optimisations

### Cache des dépendances

Le workflow utilise déjà le cache pip :

```yaml
- uses: actions/setup-python@v5
  with:
    cache: 'pip'
```

### Tests parallèles

Ajoutez `-n auto` à pytest pour paralléliser :

```yaml
- name: Run tests
  run: pytest -n auto --cov=. --cov-report=xml
```

### Matrice stratégique

Testez seulement les combinaisons importantes :

```yaml
strategy:
  matrix:
    include:
      - os: ubuntu-latest
        python-version: '3.11'
      - os: windows-latest
        python-version: '3.11'
      - os: macos-latest
        python-version: '3.11'
```

## 🔗 Ressources

- [Documentation GitHub Actions](https://docs.github.com/actions)
- [Marketplace Actions](https://github.com/marketplace?type=actions)
- [Codecov Documentation](https://docs.codecov.com/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)

## ✅ Checklist de mise en route

- [ ] Vérifier que `.github/workflows/tests.yml` existe
- [ ] Pousser le code sur GitHub
- [ ] Vérifier que le workflow s'exécute dans l'onglet Actions
- [ ] (Optionnel) Configurer les secrets GitHub
- [ ] (Optionnel) Activer Codecov
- [ ] Ajouter les badges au README
- [ ] Vérifier que tous les tests passent ✅
