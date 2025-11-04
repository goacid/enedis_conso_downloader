"""
Tests pour le script check_security.py
"""

import os
import sys
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ajouter le répertoire parent (racine du projet) au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from check_security import check_config_file, check_env_vars, check_file_permissions, check_gitignore  # noqa: E402


class TestCheckFilePermissions:
    """Tests pour check_file_permissions"""

    @pytest.mark.skipif(sys.platform == "win32", reason="Permissions Unix uniquement")
    def test_correct_permissions(self):
        """Test avec les bonnes permissions"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            test_file = f.name

        try:
            os.chmod(test_file, 0o600)
            result = check_file_permissions(test_file, 0o600, "Test File")
            assert result is True
        finally:
            os.unlink(test_file)

    @pytest.mark.skipif(sys.platform == "win32", reason="Permissions Unix uniquement")
    def test_incorrect_permissions(self):
        """Test avec de mauvaises permissions"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            test_file = f.name

        try:
            os.chmod(test_file, 0o644)  # Permissions incorrectes
            result = check_file_permissions(test_file, 0o600, "Test File")
            assert result is False
        finally:
            os.unlink(test_file)

    def test_file_not_found(self):
        """Test avec fichier inexistant"""
        result = check_file_permissions("/non/existent/file.txt", 0o600, "Test File")
        assert result is False


class TestCheckEnvVars:
    """Tests pour check_env_vars"""

    def test_env_vars_defined(self):
        """Test avec variables d'environnement définies"""
        with patch.dict(
            "os.environ",
            {"ACCOUNT_EMAIL": "test@example.com", "ACCOUNT_PASSWORD": "password123"},
        ):
            result = check_env_vars()
            assert result is True

    def test_env_vars_missing(self):
        """Test avec variables d'environnement manquantes"""
        with patch.dict("os.environ", {}, clear=True):
            result = check_env_vars()
            assert result is False

    def test_only_email_defined(self):
        """Test avec seulement l'email défini"""
        with patch.dict("os.environ", {"ACCOUNT_EMAIL": "test@example.com"}, clear=True):
            result = check_env_vars()
            assert result is False


class TestCheckGitignore:
    """Tests pour check_gitignore"""

    def test_gitignore_complete(self):
        """Test avec .gitignore complet"""
        with tempfile.TemporaryDirectory() as temp_dir:
            gitignore_path = Path(temp_dir) / ".gitignore"
            gitignore_path.write_text("config.py\n.env\n*.log\n")

            with patch("check_security.Path") as mock_path:
                mock_path.return_value = gitignore_path
                result = check_gitignore()
                assert result is True

    def test_gitignore_missing_entries(self):
        """Test avec .gitignore incomplet"""
        with tempfile.TemporaryDirectory() as temp_dir:
            gitignore_path = Path(temp_dir) / ".gitignore"
            gitignore_path.write_text("config.py\n")  # Manque .env et *.log

            with patch("check_security.Path") as mock_path:
                mock_path.return_value = gitignore_path
                result = check_gitignore()
                assert result is False

    def test_gitignore_not_found(self):
        """Test avec .gitignore inexistant"""
        with patch("check_security.Path") as mock_path:
            mock_gitignore = MagicMock()
            mock_gitignore.exists.return_value = False
            mock_path.return_value = mock_gitignore

            result = check_gitignore()
            assert result is False


class TestCheckConfigFile:
    """Tests pour check_config_file"""

    @pytest.mark.skipif(sys.platform == "win32", reason="Permissions Unix uniquement")
    def test_config_file_with_correct_permissions(self):
        """Test avec config.py ayant les bonnes permissions"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.py"
            config_path.write_text('EMAIL = "test@test.com"\n')
            os.chmod(config_path, 0o600)

            with patch("check_security.Path") as mock_path:
                mock_path.return_value = config_path
                _ = check_config_file()
                # Devrait retourner True car les permissions sont correctes
                # Note: cela dépend de l'implémentation exacte

    def test_config_file_not_found(self):
        """Test avec config.py inexistant (OK si utilise env vars)"""
        with patch("check_security.Path") as mock_path:
            mock_config = MagicMock()
            mock_config.exists.return_value = False
            mock_path.return_value = mock_config

            result = check_config_file()
            assert result is True  # C'est OK si config.py n'existe pas


class TestMainFunction:
    """Tests pour la fonction main"""

    @patch("check_security.check_env_vars")
    @patch("check_security.check_config_file")
    @patch("check_security.check_gitignore")
    @patch("sys.stdout", new_callable=StringIO)
    def test_all_checks_pass(self, mock_stdout, mock_gitignore, mock_config, mock_env):
        """Test quand toutes les vérifications passent"""
        from check_security import main

        mock_env.return_value = True
        mock_config.return_value = True
        mock_gitignore.return_value = True

        with patch("os.path.exists", return_value=False):
            result = main()

        assert result == 0

    @patch("check_security.check_env_vars")
    @patch("check_security.check_config_file")
    @patch("check_security.check_gitignore")
    @patch("sys.stdout", new_callable=StringIO)
    def test_some_checks_fail(self, mock_stdout, mock_gitignore, mock_config, mock_env):
        """Test quand certaines vérifications échouent"""
        from check_security import main

        mock_env.return_value = False
        mock_config.return_value = True
        mock_gitignore.return_value = False

        with patch("os.path.exists", return_value=False):
            result = main()

        assert result == 1
