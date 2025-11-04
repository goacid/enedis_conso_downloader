"""
Tests pour la configuration du driver Selenium
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestSetupDriver:
    """Tests pour la fonction setup_driver"""

    @patch("conso_downloader.webdriver.Chrome")
    def test_setup_driver_creates_download_dir(self, mock_chrome):
        """Test que setup_driver crée le répertoire de téléchargement"""
        from conso_downloader import setup_driver

        with tempfile.TemporaryDirectory() as temp_dir:
            download_dir = os.path.join(temp_dir, "test_downloads")

            mock_driver = MagicMock()
            mock_chrome.return_value = mock_driver

            _ = setup_driver(download_dir=download_dir, headless=False)

            assert os.path.exists(download_dir)
            assert mock_chrome.called

    @patch("conso_downloader.webdriver.Chrome")
    def test_setup_driver_headless_mode(self, mock_chrome):
        """Test du mode headless"""
        from conso_downloader import setup_driver

        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        with tempfile.TemporaryDirectory() as temp_dir:
            _ = setup_driver(download_dir=temp_dir, headless=True)

            # Vérifier que Chrome est appelé avec les bonnes options
            assert mock_chrome.called
            options = mock_chrome.call_args[1]["options"]
            # Vérifier que l'option headless est présente
            assert any("--headless" in arg for arg in options.arguments)

    @patch("conso_downloader.webdriver.Chrome")
    def test_setup_driver_visible_mode(self, mock_chrome):
        """Test du mode visible (non-headless)"""
        from conso_downloader import setup_driver

        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        with tempfile.TemporaryDirectory() as temp_dir:
            _ = setup_driver(download_dir=temp_dir, headless=False)

            # Vérifier que Chrome est appelé
            assert mock_chrome.called

    @patch("conso_downloader.webdriver.Chrome")
    def test_setup_driver_sets_window_size(self, mock_chrome):
        """Test que la taille de fenêtre est définie"""
        from conso_downloader import setup_driver

        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        with tempfile.TemporaryDirectory() as temp_dir:
            _ = setup_driver(download_dir=temp_dir)

            mock_driver.set_window_size.assert_called_once()

    @patch("conso_downloader.webdriver.Chrome")
    def test_setup_driver_anti_detection(self, mock_chrome):
        """Test que les mécanismes anti-détection sont configurés"""
        from conso_downloader import setup_driver

        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        with tempfile.TemporaryDirectory() as temp_dir:
            _ = setup_driver(download_dir=temp_dir)

            # Vérifier que execute_cdp_cmd est appelé pour le User-Agent
            assert mock_driver.execute_cdp_cmd.called
            # Vérifier que execute_script est appelé pour masquer webdriver
            assert mock_driver.execute_script.called
