"""
Tests des fonctions utilitaires
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

# Ajouter le répertoire racine du projet au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import avec gestion des dépendances
with patch.dict("os.environ", {"ACCOUNT_EMAIL": "test@test.com", "ACCOUNT_PASSWORD": "test123"}):
    from conso_downloader import USER_AGENTS, get_random_user_agent, mask_sensitive_data, split_date_range, validate_date_range


class TestMaskSensitiveData:
    """Tests pour la fonction mask_sensitive_data"""

    def test_mask_email(self):
        """Test du masquage d'email"""
        result = mask_sensitive_data("john.doe@example.com", "email")
        assert result == "jo***@example.com"

    def test_mask_short_email(self):
        """Test du masquage d'email court"""
        result = mask_sensitive_data("a@b.com", "email")
        assert result == "a***@b.com"

    def test_mask_password(self):
        """Test du masquage de mot de passe"""
        result = mask_sensitive_data("MySecretPassword123", "password")
        assert result == "************"
        assert len(result) == 12

    def test_mask_short_password(self):
        """Test du masquage de mot de passe court"""
        result = mask_sensitive_data("abc", "password")
        assert result == "***"

    def test_mask_generic(self):
        """Test du masquage générique"""
        result = mask_sensitive_data("SensitiveData123", "generic")
        assert result == "Sen***"

    def test_mask_empty_string(self):
        """Test du masquage de chaîne vide"""
        result = mask_sensitive_data("", "email")
        assert result == "***"

    def test_mask_none(self):
        """Test du masquage de None"""
        result = mask_sensitive_data(None, "email")
        assert result == "***"


class TestValidateDateRange:
    """Tests pour la fonction validate_date_range"""

    def test_valid_dates(self):
        """Test avec des dates valides"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 7)
        result_start, result_end = validate_date_range(start, end)
        assert result_start == start
        assert result_end == end

    def test_none_dates_uses_defaults(self):
        """Test avec des dates None (utilise les valeurs par défaut)"""
        result_start, result_end = validate_date_range(None, None)
        assert isinstance(result_start, datetime)
        assert isinstance(result_end, datetime)
        assert result_start < result_end
        # Devrait être environ 7 jours
        assert (result_end - result_start).days == 6

    def test_start_after_end_raises_error(self):
        """Test avec date début après date fin"""
        start = datetime(2024, 1, 10)
        end = datetime(2024, 1, 1)
        with pytest.raises(ValueError, match="postérieure"):
            validate_date_range(start, end)

    def test_future_end_date_raises_error(self):
        """Test avec date de fin dans le futur"""
        start = datetime.now() - timedelta(days=7)
        end = datetime.now() + timedelta(days=1)
        with pytest.raises(ValueError, match="futur"):
            validate_date_range(start, end)

    def test_period_too_long_raises_error(self):
        """Test avec période trop longue (>365 jours)"""
        start = datetime(2023, 1, 1)
        end = datetime(2024, 2, 1)
        with pytest.raises(ValueError, match="trop longue"):
            validate_date_range(start, end)

    def test_one_day_period(self):
        """Test avec une période d'un jour"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 1)
        result_start, result_end = validate_date_range(start, end)
        assert result_start == start
        assert result_end == end


class TestGetRandomUserAgent:
    """Tests pour la fonction get_random_user_agent"""

    def test_returns_valid_user_agent(self):
        """Test que la fonction retourne un user agent valide"""
        ua = get_random_user_agent()
        assert ua in USER_AGENTS
        assert len(ua) > 0

    def test_returns_different_values(self):
        """Test que la fonction peut retourner différentes valeurs"""
        # Générer plusieurs user agents
        agents = [get_random_user_agent() for _ in range(20)]
        # Il devrait y avoir au moins 2 valeurs différentes (probabilité très élevée)
        assert len(set(agents)) > 1 or len(USER_AGENTS) == 1


class TestSplitDateRange:
    """Tests pour la fonction split_date_range"""

    def test_period_smaller_than_max_days(self):
        """Test avec période < max_days"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 5)
        periods = split_date_range(start, end, max_days=7)
        assert len(periods) == 1
        assert periods[0] == (start, end)

    def test_period_equal_to_max_days(self):
        """Test avec période = max_days"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 7)
        periods = split_date_range(start, end, max_days=7)
        assert len(periods) == 1
        assert periods[0] == (start, end)

    def test_period_larger_than_max_days(self):
        """Test avec période > max_days"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 15)
        periods = split_date_range(start, end, max_days=7)
        # 15 jours devrait être divisé en 3 périodes (7j + 7j + 1j)
        assert len(periods) == 3
        assert periods[0] == (datetime(2024, 1, 1), datetime(2024, 1, 7))
        assert periods[1] == (datetime(2024, 1, 8), datetime(2024, 1, 14))
        assert periods[2] == (datetime(2024, 1, 15), datetime(2024, 1, 15))

    def test_one_day_period(self):
        """Test avec une période d'un jour"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 1)
        periods = split_date_range(start, end, max_days=7)
        assert len(periods) == 1
        assert periods[0] == (start, end)

    def test_exactly_two_periods(self):
        """Test avec exactement deux périodes"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 8)
        periods = split_date_range(start, end, max_days=7)
        assert len(periods) == 2
        assert periods[0] == (datetime(2024, 1, 1), datetime(2024, 1, 7))
        assert periods[1] == (datetime(2024, 1, 8), datetime(2024, 1, 8))

    def test_month_long_period(self):
        """Test avec une période d'un mois"""
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 31)
        periods = split_date_range(start, end, max_days=7)
        # 31 jours = 5 périodes (7+7+7+7+3)
        assert len(periods) == 5
        # Vérifier que toutes les périodes sont couvertes
        assert periods[0][0] == start
        assert periods[-1][1] == end
        # Vérifier la continuité
        for i in range(len(periods) - 1):
            assert periods[i][1] + timedelta(days=1) == periods[i + 1][0]
