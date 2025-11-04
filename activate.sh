#!/bin/bash
# Script d'activation rapide de l'environnement virtuel

if [ ! -d ".venv" ]; then
    echo "❌ Environnement virtuel non trouvé"
    echo "Lancez d'abord: ./install.sh"
    exit 1
fi

echo "🔄 Activation de l'environnement virtuel..."
source .venv/bin/activate

echo "✅ Environnement virtuel activé"
echo ""
echo "📋 Commandes disponibles:"
echo "  • python test_setup.py                    # Tester la configuration"
echo "  • python enedis_downloader.py --help     # Voir l'aide"
echo "  • deactivate                             # Désactiver l'environnement"
echo ""
echo "💡 Exemple d'utilisation:"
echo "  python enedis_downloader.py --start \"2024-01-01\" --end \"2024-01-07\" --debug"
echo ""
echo "⚠️  IMPORTANT: Ce script doit être lancé avec 'source' pour fonctionner:"
echo "   source ./activate.sh"
echo "   (ou: . ./activate.sh)"