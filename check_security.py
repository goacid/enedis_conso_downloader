#!/usr/bin/env python3
"""
Script de vérification de la configuration de sécurité
Vérifie que tous les éléments de sécurité sont en place
"""

import os
import stat
import sys
from pathlib import Path


def check_file_permissions(filepath: str, expected_mode: int, name: str) -> bool:
    """Vérifie les permissions d'un fichier"""
    if not os.path.exists(filepath):
        print(f"⚠️  {name}: Fichier non trouvé ({filepath})")
        return False

    file_stat = os.stat(filepath)
    file_mode = stat.S_IMODE(file_stat.st_mode)

    if file_mode == expected_mode:
        print(f"✅ {name}: Permissions OK ({oct(file_mode)})")
        return True
    else:
        print(f"❌ {name}: Permissions incorrectes (actuel: {oct(file_mode)}, attendu: {oct(expected_mode)})")
        print(f"   Corriger avec: chmod {oct(expected_mode)[2:]} {filepath}")
        return False


def check_env_vars() -> bool:
    """Vérifie si les variables d'environnement sont définies"""
    email = os.getenv("ACCOUNT_EMAIL")
    password = os.getenv("ACCOUNT_PASSWORD")

    if email and password:
        print("✅ Variables d'environnement: Définies")
        print(f"   ACCOUNT_EMAIL: {email[:3]}***@{email.split('@')[1] if '@' in email else '***'}")
        print(f"   ACCOUNT_PASSWORD: {'*' * 12}")
        return True
    else:
        print("⚠️  Variables d'environnement: Non définies")
        print("   Vérifiez config.py en fallback...")
        return False


def check_gitignore() -> bool:
    """Vérifie que .gitignore contient les fichiers sensibles"""
    gitignore_path = Path(".gitignore")

    if not gitignore_path.exists():
        print("❌ .gitignore: Non trouvé")
        return False

    content = gitignore_path.read_text()
    required = ["config.py", ".env", "*.log"]
    missing = [r for r in required if r not in content]

    if not missing:
        print("✅ .gitignore: Tous les fichiers sensibles exclus")
        return True
    else:
        print(f"❌ .gitignore: Fichiers manquants: {', '.join(missing)}")
        return False


def check_config_file() -> bool:
    """Vérifie si config.py existe et a les bonnes permissions"""
    config_path = Path("config.py")

    if not config_path.exists():
        print("⚠️  config.py: Non trouvé (OK si utilise variables d'env)")
        return True

    # Vérifier permissions (devrait être 600)
    return check_file_permissions("config.py", 0o600, "config.py")


def main():
    """Point d'entrée principal"""
    print("=" * 70)
    print("🔒 VÉRIFICATION DE LA CONFIGURATION DE SÉCURITÉ")
    print("=" * 70)
    print()

    checks = []

    # 1. Variables d'environnement
    print("📋 1. Variables d'Environnement")
    print("-" * 70)
    checks.append(check_env_vars())
    print()

    # 2. Fichier config.py
    print("📋 2. Fichier de Configuration")
    print("-" * 70)
    checks.append(check_config_file())
    print()

    # 3. .gitignore
    print("📋 3. Exclusion Git")
    print("-" * 70)
    checks.append(check_gitignore())
    print()

    # 4. Permissions des fichiers sensibles
    print("📋 4. Permissions des Fichiers")
    print("-" * 70)

    # Logs
    if os.path.exists("downloader.log"):
        checks.append(check_file_permissions("downloader.log", 0o600, "Logs"))
    else:
        print("⚠️  downloader.log: Non trouvé (normal si jamais exécuté)")

    # Downloads directory
    if os.path.exists("downloads"):
        checks.append(check_file_permissions("downloads", 0o700, "Downloads"))
    else:
        print("⚠️  downloads/: Non trouvé (sera créé au premier téléchargement)")

    # .env file
    if os.path.exists(".env"):
        checks.append(check_file_permissions(".env", 0o600, ".env"))
    else:
        print("⚠️  .env: Non trouvé (OK si utilise config.py ou variables d'env)")

    print()

    # 5. Résumé
    print("=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)

    success_count = sum(checks)
    total_count = len(checks)

    if success_count == total_count:
        print(f"✅ TOUTES LES VÉRIFICATIONS RÉUSSIES ({success_count}/{total_count})")
        print()
        print("🎉 Configuration sécurisée - Prêt pour la production !")
        return 0
    else:
        print(f"⚠️  VÉRIFICATIONS PARTIELLES ({success_count}/{total_count})")
        print()
        print("📖 Consultez SECURITY.md pour les recommandations")
        return 1


if __name__ == "__main__":
    sys.exit(main())
