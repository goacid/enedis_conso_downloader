"""
Configuration et fixtures pour pytest
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Ajouter le répertoire racine du projet au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@pytest.fixture
def temp_download_dir():
    """Crée un répertoire temporaire pour les téléchargements"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_driver():
    """Mock du WebDriver Selenium"""
    driver = MagicMock()
    driver.find_element.return_value = MagicMock()
    driver.find_elements.return_value = []
    driver.execute_script.return_value = None
    driver.switch_to.frame.return_value = None
    driver.get.return_value = None
    return driver


@pytest.fixture
def mock_wait():
    """Mock de WebDriverWait"""
    wait = MagicMock()
    wait.until.return_value = MagicMock()
    return wait


@pytest.fixture
def sample_config():
    """Configuration de test"""
    return {
        "EMAIL": "test@example.com",
        "PASSWORD": "TestPassword123!",
        "BASE_URL": "https://mon-compte-particulier.enedis.fr/",
    }


@pytest.fixture
def set_env_vars(sample_config):
    """Définit les variables d'environnement pour les tests"""
    os.environ["ACCOUNT_EMAIL"] = sample_config["EMAIL"]
    os.environ["ACCOUNT_PASSWORD"] = sample_config["PASSWORD"]
    os.environ["BASE_URL"] = sample_config["BASE_URL"]
    yield
    # Nettoyage
    for key in ["ACCOUNT_EMAIL", "ACCOUNT_PASSWORD", "BASE_URL"]:
        os.environ.pop(key, None)


@pytest.fixture
def mock_selenium_element():
    """Mock d'un élément Selenium"""
    element = MagicMock()
    element.is_displayed.return_value = True
    element.is_enabled.return_value = True
    element.text = "Test Text"
    element.get_attribute.return_value = "test-value"
    element.send_keys.return_value = None
    element.clear.return_value = None
    element.click.return_value = None
    return element
