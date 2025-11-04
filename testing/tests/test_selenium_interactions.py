"""
Tests des interactions Selenium
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestAcceptCookies:
    """Tests pour la fonction accept_cookies"""

    @patch("conso_downloader.WebDriverWait")
    def test_accept_cookies_success(self, mock_wait_class):
        """Test d'acceptation réussie des cookies"""
        from conso_downloader import accept_cookies

        # Setup
        mock_driver = MagicMock()
        mock_button = MagicMock()
        mock_wait = MagicMock()
        mock_wait.until.return_value = mock_button
        mock_wait_class.return_value = mock_wait

        # Test
        result = accept_cookies(mock_driver, "test_button_id")

        # Vérifications
        assert result is True
        mock_driver.execute_script.assert_called_once()

    @patch("conso_downloader.WebDriverWait")
    @patch("conso_downloader.TimeoutException", Exception)
    def test_accept_cookies_timeout(self, mock_wait_class):
        """Test quand le popup n'apparaît pas"""
        from conso_downloader import accept_cookies

        # Setup
        mock_driver = MagicMock()
        mock_wait = MagicMock()
        mock_wait.until.side_effect = Exception("Timeout")
        mock_wait_class.return_value = mock_wait

        # Test
        result = accept_cookies(mock_driver)

        # Vérifications
        assert result is False


class TestLoginStep1Email:
    """Tests pour la fonction login_step1_email"""

    @patch("conso_downloader.WebDriverWait")
    @patch("conso_downloader.time.sleep")
    def test_login_step1_success(self, mock_sleep, mock_wait_class):
        """Test de saisie email réussie"""
        from conso_downloader import login_step1_email

        # Setup
        mock_driver = MagicMock()
        mock_email_field = MagicMock()
        mock_button = MagicMock()
        mock_button.is_enabled.return_value = True

        mock_wait = MagicMock()
        mock_wait.until.return_value = mock_email_field
        mock_wait_class.return_value = mock_wait

        mock_driver.find_element.return_value = mock_button

        # Test
        result = login_step1_email(mock_driver, "test@example.com")

        # Vérifications
        assert result is True
        mock_email_field.clear.assert_called_once()
        mock_email_field.send_keys.assert_called_once_with("test@example.com")

    @patch("conso_downloader.WebDriverWait")
    def test_login_step1_failure(self, mock_wait_class):
        """Test d'échec de saisie email"""
        from conso_downloader import login_step1_email

        # Setup
        mock_driver = MagicMock()
        mock_wait = MagicMock()
        mock_wait.until.side_effect = Exception("Element not found")
        mock_wait_class.return_value = mock_wait

        # Test
        result = login_step1_email(mock_driver, "test@example.com")

        # Vérifications
        assert result is False


class TestLoginStep2Password:
    """Tests pour la fonction login_step2_password"""

    @patch("conso_downloader.WebDriverWait")
    @patch("conso_downloader.time.sleep")
    def test_login_step2_success(self, mock_sleep, mock_wait_class):
        """Test de saisie mot de passe réussie"""
        from conso_downloader import login_step2_password

        # Setup
        mock_driver = MagicMock()
        mock_password_field = MagicMock()
        mock_button = MagicMock()

        mock_wait = MagicMock()
        mock_wait.until.return_value = mock_password_field
        mock_wait_class.return_value = mock_wait

        mock_driver.find_element.return_value = mock_button

        # Test
        result = login_step2_password(mock_driver, "password123")

        # Vérifications
        assert result is True
        mock_password_field.clear.assert_called_once()
        mock_password_field.send_keys.assert_called_once_with("password123")

    @patch("conso_downloader.WebDriverWait")
    def test_login_step2_failure(self, mock_wait_class):
        """Test d'échec de saisie mot de passe"""
        from conso_downloader import login_step2_password

        # Setup
        mock_driver = MagicMock()
        mock_wait = MagicMock()
        mock_wait.until.side_effect = Exception("Element not found")
        mock_wait_class.return_value = mock_wait

        # Test
        result = login_step2_password(mock_driver, "password123")

        # Vérifications
        assert result is False


class TestNavigateToConsumption:
    """Tests pour la fonction navigate_to_consumption"""

    @patch("conso_downloader.accept_cookies")
    @patch("conso_downloader.WebDriverWait")
    @patch("conso_downloader.time.sleep")
    def test_navigate_success(self, mock_sleep, mock_wait_class, mock_accept_cookies):
        """Test de navigation réussie"""
        from conso_downloader import navigate_to_consumption

        # Setup
        mock_driver = MagicMock()

        # Mock bouton "Ma consommation"
        mock_menu_button = MagicMock()
        mock_menu_button.is_displayed.return_value = True
        mock_menu_button.text = "Ma consommation"

        # Mock lien "Suivre ma consommation"
        mock_link = MagicMock()
        mock_link.is_displayed.return_value = True
        mock_link.text = "Suivre ma consommation"

        mock_driver.find_elements.side_effect = [
            [mock_menu_button],  # Première recherche de boutons
            [mock_link],  # Recherche de liens
        ]

        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait

        # Test
        result = navigate_to_consumption(mock_driver)

        # Vérifications
        assert result is True
        mock_accept_cookies.assert_called_once()


class TestSwitchToIframe:
    """Tests pour la fonction switch_to_iframe"""

    @patch("conso_downloader.WebDriverWait")
    def test_switch_to_iframe_success(self, mock_wait_class):
        """Test de basculement réussi vers iframe"""
        from conso_downloader import switch_to_iframe

        # Setup
        mock_driver = MagicMock()
        mock_iframe = MagicMock()
        mock_iframe.get_attribute.return_value = "https://example.com/mes-mesures"

        mock_driver.find_elements.return_value = [mock_iframe]
        mock_driver.execute_script.return_value = "complete"

        mock_wait = MagicMock()
        mock_wait.until.return_value = None
        mock_wait_class.return_value = mock_wait

        # Test
        result = switch_to_iframe(mock_driver)

        # Vérifications
        assert result is True
        mock_driver.switch_to.frame.assert_called_once_with(mock_iframe)

    @patch("conso_downloader.WebDriverWait")
    def test_switch_to_iframe_not_found(self, mock_wait_class):
        """Test quand iframe n'est pas trouvée"""
        from conso_downloader import switch_to_iframe

        # Setup
        mock_driver = MagicMock()
        mock_driver.find_elements.return_value = []

        mock_wait = MagicMock()
        mock_wait.until.side_effect = Exception("Timeout")
        mock_wait_class.return_value = mock_wait

        # Test
        result = switch_to_iframe(mock_driver)

        # Vérifications
        assert result is False


class TestSelectHeuresMode:
    """Tests pour la fonction select_heures_mode"""

    @patch("conso_downloader.WebDriverWait")
    @patch("conso_downloader.time.sleep")
    def test_select_heures_mode_success(self, mock_sleep, mock_wait_class):
        """Test de sélection mode Heures réussie"""
        from conso_downloader import select_heures_mode

        # Setup
        mock_driver = MagicMock()
        mock_span = MagicMock()
        mock_span.is_displayed.return_value = True
        mock_span.text = "Heures"
        mock_label = MagicMock()
        mock_span.find_element.return_value = mock_label

        mock_driver.find_elements.return_value = [mock_span]

        mock_wait = MagicMock()
        mock_wait_class.return_value = mock_wait

        # Test
        result = select_heures_mode(mock_driver)

        # Vérifications
        assert result is True
        mock_driver.execute_script.assert_called_once()

    def test_select_heures_mode_not_found(self):
        """Test quand bouton Heures n'est pas trouvé"""
        from conso_downloader import select_heures_mode

        # Setup
        mock_driver = MagicMock()
        mock_driver.find_elements.return_value = []

        # Test
        result = select_heures_mode(mock_driver)

        # Vérifications
        assert result is False
