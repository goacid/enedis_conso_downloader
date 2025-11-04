"""
Configuration pour le récupérateur de données Enedis
Copiez ce fichier vers config.py et renseignez vos informations
"""

# Identifiants Enedis, remplacez par vos vraies valeurs ou utilisez des variables d'environnement
EMAIL = "em@mai.l"
PASSWORD = "XXXXXXX!%"

# Configuration du navigateur
CHROME_DRIVER_PATH = None  # None pour utiliser le PATH système, ou chemin vers chromedriver
FIREFOX_DRIVER_PATH = None  # Alternative Firefox
BROWSER = "chrome"  # "chrome" ou "firefox"

# Dossiers et fichiers
DOWNLOAD_DIR = "./downloads"
LOG_FILE = "./downloader.log"

# Timeouts (en secondes)
PAGE_LOAD_TIMEOUT = 30
ELEMENT_TIMEOUT = 15
DOWNLOAD_TIMEOUT = 60

# Options avancées
DEBUG_MODE = False
HEADLESS_MODE = True
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 2  # Délai entre les requêtes en secondes

# URLs Enedis
# Point d'entrée principal (popup cookies #1 puis redirige vers mon-compte.enedis.fr)
BASE_URL = "https://mon-compte-particulier.enedis.fr/"
# URL après redirection (popup cookies #2 + formulaire login)
LOGIN_URL = "https://mon-compte.enedis.fr/"
MEASURES_URL = "https://mon-compte-particulier.enedis.fr/suivi-de-consommation"

# Sélecteurs CSS (peut nécessiter une mise à jour si l'interface change)
SELECTORS = {
    # Boutons cookies (TrustCommander)
    "cookie_accept": "#popin_tc_privacy_button_3, button[id*='tc_privacy_button_3']",
    "cookie_refuse": "#popin_tc_privacy_button_2, button[id*='tc_privacy_button_2']",
    "cookie_customize": "#popin_tc_privacy_button, button[id*='tc_privacy_button']",
    # Login - Étape 1 : Email uniquement
    "login_email": "#idToken1, input[type='email'], input[name='callback_0']",
    "login_email_submit": "#idToken3_0, input[value='Suivant'], input[type='submit']",
    # Login - Étape 2 : Password (après validation email)
    "login_password": "#idToken2, input[type='password'], input[name='callback_1']",
    "login_password_submit": "input[type='submit'], button[type='submit'], input[value='Se connecter']",
    # Captcha FriendlyCaptcha (résolu automatiquement)
    "captcha_widget": "#captcha-widget, .frc-container",
    "captcha_solution": "input[name='frc-captcha-solution']",
    # Mesures
    "iframe_measures": "iframe[title*='mes-mesures']",
    "download_button": "button.lnc-btn-secondary-white",
    "date_start": "input[type='date']",
    "date_end": "input[type='date']",
    "visualiser_button": "button",
}

# Format des données
DATA_FORMAT = "30min"  # Format des données à télécharger
FILE_PREFIX = "conso_30min"  # Préfixe des fichiers téléchargés
