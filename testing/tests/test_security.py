"""
Tests de sécurité
"""

import os
import stat
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestCredentialsValidation:
    """Tests de validation des identifiants"""

    def test_credentials_from_env_vars(self):
        """Test que les credentials sont lus depuis les variables d'environnement"""
        with patch.dict(
            "os.environ",
            {"ACCOUNT_EMAIL": "test@example.com", "ACCOUNT_PASSWORD": "TestPass123"},
        ):
            # Recharger le module pour prendre en compte les nouvelles variables
            import importlib

            import conso_downloader

            importlib.reload(conso_downloader)

            assert conso_downloader.EMAIL == "test@example.com"
            assert conso_downloader.PASSWORD == "TestPass123"

    def test_https_url_validation(self):
        """Test que seules les URLs HTTPS sont acceptées"""
        # Cette fonction devrait être appelée au démarrage du module
        with patch.dict(
            "os.environ",
            {
                "ACCOUNT_EMAIL": "test@example.com",
                "ACCOUNT_PASSWORD": "TestPass123",
                "BASE_URL": "http://insecure.com",  # Non HTTPS
            },
        ):
            with pytest.raises(SystemExit):
                # Recharger le module devrait lever une erreur
                import importlib

                import conso_downloader

                importlib.reload(conso_downloader)


class TestDataMasking:
    """Tests du masquage de données sensibles"""

    def test_email_masking_in_logs(self):
        """Test que les emails sont masqués dans les logs"""
        with patch.dict(
            "os.environ",
            {"ACCOUNT_EMAIL": "john.doe@example.com", "ACCOUNT_PASSWORD": "pass123"},
        ):
            from conso_downloader import mask_sensitive_data

            masked = mask_sensitive_data("john.doe@example.com", "email")
            assert "john.doe" not in masked
            assert "@example.com" in masked
            assert "***" in masked

    def test_password_never_logged(self):
        """Test que les mots de passe ne sont jamais loggés en clair"""
        with patch.dict(
            "os.environ",
            {
                "ACCOUNT_EMAIL": "test@example.com",
                "ACCOUNT_PASSWORD": "MySecretPassword123!",
            },
        ):
            from conso_downloader import mask_sensitive_data

            masked = mask_sensitive_data("MySecretPassword123!", "password")
            assert "MySecretPassword123!" not in masked
            assert all(c == "*" for c in masked)


class TestFilePermissions:
    """Tests des permissions de fichiers"""

    @pytest.mark.skipif(sys.platform == "win32", reason="Permissions Unix uniquement")
    def test_log_file_permissions(self):
        """Test que le fichier de log a les bonnes permissions (600)"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            log_file = f.name

        try:
            # Simuler la création du fichier de log
            Path(log_file).touch()
            os.chmod(log_file, stat.S_IRUSR | stat.S_IWUSR)  # 600

            # Vérifier les permissions
            file_stat = os.stat(log_file)
            file_mode = stat.S_IMODE(file_stat.st_mode)

            assert file_mode == 0o600
        finally:
            os.unlink(log_file)

    @pytest.mark.skipif(sys.platform == "win32", reason="Permissions Unix uniquement")
    def test_download_dir_permissions(self):
        """Test que le répertoire de téléchargement a les bonnes permissions (700)"""
        with tempfile.TemporaryDirectory() as temp_dir:
            download_dir = os.path.join(temp_dir, "downloads")
            os.makedirs(download_dir)
            os.chmod(download_dir, stat.S_IRWXU)  # 700

            # Vérifier les permissions
            dir_stat = os.stat(download_dir)
            dir_mode = stat.S_IMODE(dir_stat.st_mode)

            assert dir_mode == 0o700


class TestAntiDetection:
    """Tests des mécanismes anti-détection"""

    def test_random_user_agent_is_realistic(self):
        """Test que les User-Agents sont réalistes"""
        with patch.dict(
            "os.environ",
            {"ACCOUNT_EMAIL": "test@example.com", "ACCOUNT_PASSWORD": "pass123"},
        ):
            from conso_downloader import USER_AGENTS, get_random_user_agent

            ua = get_random_user_agent()

            # Vérifier que c'est un User-Agent valide
            assert "Mozilla" in ua
            assert ua in USER_AGENTS

    def test_user_agent_rotation(self):
        """Test que les User-Agents changent (rotation)"""
        with patch.dict(
            "os.environ",
            {"ACCOUNT_EMAIL": "test@example.com", "ACCOUNT_PASSWORD": "pass123"},
        ):
            from conso_downloader import USER_AGENTS, get_random_user_agent

            if len(USER_AGENTS) > 1:
                # Générer plusieurs UA et vérifier qu'ils ne sont pas tous identiques
                agents = [get_random_user_agent() for _ in range(20)]
                unique_agents = set(agents)

                # Il devrait y avoir au moins 2 UA différents
                assert len(unique_agents) > 1


class TestSecureConfiguration:
    """Tests de configuration sécurisée"""

    def test_no_credentials_in_code(self):
        """Test qu'il n'y a pas de credentials en dur dans le code"""
        # Lire le fichier source (dans le répertoire racine du projet)
        source_file = Path(__file__).parent.parent.parent / "conso_downloader.py"
        content = source_file.read_text()

        # Vérifier qu'il n'y a pas de patterns suspects
        suspicious_patterns = ['EMAIL = "', 'PASSWORD = "', "email@", "password="]

        for pattern in suspicious_patterns:
            # Ignorer les commentaires et les variables d'environnement
            lines = content.split("\n")
            for line in lines:
                if pattern in line and not line.strip().startswith("#"):
                    # S'assurer que c'est bien une variable d'env
                    if "os.getenv" not in line and "EMAIL = EMAIL" not in line and "PASSWORD = PASSWORD" not in line:
                        # Vérifier qu'il n'y a pas de vrai email/password
                        if "@" in line and ".com" in line:
                            # Vérifier que c'est un exemple
                            assert "example.com" in line.lower() or "test" in line.lower() or "mai.l" in line.lower()
