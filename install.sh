#!/bin/bash

# Script d'installation pour le récupérateur de données de consommation electrique avec environnement virtuel

set -e

echo "🔧 Installation du récupérateur de données de consommation electrique avec environnement virtuel..."

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    echo "Installation: sudo apt-get install python3 python3-venv python3-pip"
    exit 1
fi

echo "✅ Python 3 détecté: $(python3 --version)"

# Créer environnement virtuel si inexistant
if [ ! -d ".venv" ]; then
    echo "🔧 Création de l'environnement virtuel..."
    python3 -m venv .venv
    echo "✅ Environnement virtuel créé"
else
    echo "✅ Environnement virtuel déjà existant"
fi

# Activer l'environnement virtuel
echo "🔄 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Mettre à jour pip
echo "📦 Mise à jour de pip..."
pip install --upgrade pip

# Installation des dépendances Python dans l'environnement virtuel
echo "📦 Installation des dépendances Python dans l'environnement virtuel..."
pip install -r requirements.txt

# Installation de ChromeDriver (Ubuntu/Debian)
if command -v apt-get &> /dev/null; then
    echo "🌐 Installation de ChromeDriver..."
    sudo apt-get update
    sudo apt-get install -y chromium-chromedriver
    
    # Vérifier l'installation
    if command -v chromedriver &> /dev/null; then
        echo "✅ ChromeDriver installé: $(chromedriver --version)"
    else
        echo "⚠️  ChromeDriver non trouvé dans PATH, installation manuelle nécessaire"
        echo "Téléchargez depuis: https://chromedriver.chromium.org/"
    fi
else
    echo "⚠️  Système non Debian/Ubuntu détecté"
    echo "Installation manuelle de ChromeDriver nécessaire:"
    echo "https://chromedriver.chromium.org/"
fi

# Création du fichier de configuration
if [ ! -f "config.py" ]; then
    echo "⚙️  Création du fichier de configuration..."
    cp config.example.py config.py
    echo "✅ Fichier config.py créé"
    echo ""
    echo "🔑 IMPORTANT: Éditez config.py et renseignez vos identifiants Enedis"
    echo "   _USERNAME = \"votre_email@example.com\""
    echo "   PASSWORD = \"votre_mot_de_passe\""
else
    echo "✅ Fichier config.py existe déjà"
fi

# Création du dossier de téléchargement
mkdir -p downloads
echo "✅ Dossier downloads créé"

echo ""
echo "🎉 Installation terminée !"
echo ""
echo "Prochaines étapes:"
echo "1. Activez l'environnement virtuel: source .venv/bin/activate"
echo "2. Éditez config.py avec vos identifiants Enedis"
echo "3. Testez la configuration: python test_setup.py"
echo "4. Premier test: python conso_downloader.py --start \"2024-01-01\" --end \"2024-01-07\" "
echo ""
echo "⚠️  N'oubliez pas d'activer l'environnement virtuel à chaque utilisation:"
echo "source .venv/bin/activate"