#!/usr/bin/env python3
"""
Récupérateur automatique de données de consommation Enedis
Version automatique sans interactions manuelles - VERSION SÉCURISÉE
"""

import logging
import os
import secrets
import stat
import sys
import time
import warnings
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from typing import Optional, Tuple

# Selenium imports
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configuration sécurisée via variables d'environnement OU config
try:
    # Priorité 1: Variables d'environnement (plus sécurisé)
    EMAIL = os.getenv("ACCOUNT_EMAIL")
    PASSWORD = os.getenv("ACCOUNT_PASSWORD")
    BASE_URL = os.getenv("BASE_URL", "https://mon-compte-particulier.enedis.fr/")

    # Priorité 2: Fichier config si variables d'env non définies
    if not EMAIL or not PASSWORD:
        from config import BASE_URL as CONFIG_BASE_URL
        from config import EMAIL as CONFIG_EMAIL
        from config import PASSWORD as CONFIG_PASSWORD

        EMAIL = EMAIL or CONFIG_EMAIL
        PASSWORD = PASSWORD or CONFIG_PASSWORD
        BASE_URL = BASE_URL or CONFIG_BASE_URL

except ImportError:
    # Si config.py n'existe pas et pas de variables d'env
    EMAIL = os.getenv("ACCOUNT_EMAIL")
    PASSWORD = os.getenv("ACCOUNT_PASSWORD")
    BASE_URL = os.getenv("BASE_URL", "https://mon-compte-particulier.enedis.fr/")

# Validation des credentials
if not EMAIL or not PASSWORD:
    print("❌ ERREUR: Identifiants non configurés!")
    print("Définissez les variables d'environnement ACCOUNT_EMAIL et ACCOUNT_PASSWORD")
    print("Ou créez un fichier config.py avec EMAIL et PASSWORD")
    sys.exit(1)

# Validation de la sécurité de l'URL
if BASE_URL and not BASE_URL.startswith("https://"):
    print("❌ ERREUR: BASE_URL doit utiliser HTTPS pour la sécurité!")
    print(f"URL fournie: {BASE_URL}")
    sys.exit(1)

# Configuration du logging avec rotation automatique
LOG_FILE = "downloader.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=10_000_000, backupCount=3),  # 10 MB max, 3 backups
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Définir les permissions du fichier log (600 = lecture/écriture propriétaire uniquement)
if os.path.exists(LOG_FILE):
    try:
        os.chmod(LOG_FILE, stat.S_IRUSR | stat.S_IWUSR)  # 600
        logger.debug("🔒 Permissions log définies: 600 (propriétaire uniquement)")
    except Exception:
        pass  # Ignorer si impossible (Windows par exemple)

# Désactiver les warnings et erreurs de fermeture de Selenium/urllib3
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.ERROR)


# Liste de User-Agents réalistes pour rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]


def get_random_user_agent() -> str:
    """Retourne un User-Agent aléatoire pour éviter la détection"""
    return secrets.choice(USER_AGENTS)


def mask_sensitive_data(data: str, mask_type: str = "email") -> str:
    """
    Masque les données sensibles pour les logs

    Args:
        data: Donnée à masquer
        mask_type: Type de masquage ('email', 'password', 'generic')

    Returns:
        Donnée masquée
    """
    if not data:
        return "***"

    if mask_type == "email":
        if "@" in data:
            local, domain = data.split("@", 1)
            return f"{local[:2]}***@{domain}"
        return "***@***"
    elif mask_type == "password":
        return "*" * min(len(data), 12)
    else:
        return f"{data[:3]}***" if len(data) > 3 else "***"


def validate_date_range(start_date: Optional[datetime], end_date: Optional[datetime]) -> Tuple[datetime, datetime]:
    """
    Valide et normalise les dates

    Args:
        start_date: Date de début
        end_date: Date de fin

    Returns:
        Tuple (start_date, end_date) validé

    Raises:
        ValueError: Si les dates sont invalides
    """
    # Calculer les dates par défaut
    if end_date is None:
        end_date = datetime.now() - timedelta(days=1)
    if start_date is None:
        start_date = end_date - timedelta(days=6)

    # Validation
    if start_date > end_date:
        raise ValueError(f"Date de début ({start_date}) postérieure à date de fin ({end_date})")

    if end_date > datetime.now():
        raise ValueError(f"Date de fin ({end_date}) dans le futur")

    if (end_date - start_date).days > 365:
        raise ValueError(f"Période trop longue (>{365} jours): {(end_date - start_date).days} jours")

    return start_date, end_date


def setup_driver(download_dir: str = None, headless: bool = False) -> webdriver.Chrome:
    """
    Configure et retourne le driver Chrome avec les options anti-détection

    Args:
        download_dir: Répertoire de téléchargement (défaut: ./downloads)
        headless: Mode sans interface graphique (défaut: False = visible)
    """

    if download_dir is None:
        download_dir = os.path.join(os.getcwd(), "downloads")

    os.makedirs(download_dir, exist_ok=True)

    options = Options()

    # Mode headless si demandé
    if headless:
        options.add_argument("--headless=new")
        logger.info("🔇 Mode headless activé (navigateur invisible)")
    else:
        logger.info("👁️  Mode visible activé (navigateur visible)")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Configuration des préférences de téléchargement
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    # Désactiver les logs Selenium pour une fermeture propre
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")  # Supprime les erreurs de fermeture

    driver = webdriver.Chrome(options=options)

    # Anti-détection via CDP avec User-Agent aléatoire
    random_ua = get_random_user_agent()
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": random_ua})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.set_window_size(1536, 864)

    logger.info(f"✅ Driver Chrome initialisé - Downloads: {download_dir}")
    logger.debug(f"🔒 User-Agent: {random_ua[:50]}...")
    return driver


def accept_cookies(driver: webdriver.Chrome, button_id: str = "popin_tc_privacy_button_3") -> bool:
    """Accepte les cookies si le popup est présent"""
    try:
        wait = WebDriverWait(driver, 5)
        cookie_button = wait.until(EC.element_to_be_clickable((By.ID, button_id)))
        driver.execute_script("arguments[0].click();", cookie_button)
        logger.info(f"✅ Popup cookies accepté: {button_id}")
        time.sleep(1)  # Courte pause pour laisser le popup se fermer
        return True
    except TimeoutException:
        logger.debug("Pas de popup cookies détecté")
        return False


def login_step1_email(driver: webdriver.Chrome, email: str) -> bool:
    """Première étape de login : saisie de l'email"""
    try:
        wait = WebDriverWait(driver, 10)

        # Attendre le champ email
        email_field = wait.until(EC.presence_of_element_located((By.ID, "idToken1")))
        email_field.clear()
        email_field.send_keys(email)
        # Ne PAS logger l'email complet - sécurité
        email_masked = email[:3] + "***@" + email.split("@")[1] if "@" in email else "***"
        logger.info(f"✅ Email saisi: {email_masked}")

        # Attendre résolution captcha en temps réel
        # Surveiller quand le bouton devient réellement cliquable (captcha résolu)
        logger.info("⏳ Attente résolution captcha...")
        start_wait = time.time()
        try:
            # Attendre que le bouton soit présent et activé (classe disabled retirée)
            WebDriverWait(driver, 30).until(lambda d: d.find_element(By.ID, "idToken3_0").is_enabled())
            elapsed = time.time() - start_wait
            logger.info(f"✅ Captcha résolu en {elapsed:.1f}s")
        except TimeoutException:
            logger.warning("⚠️ Timeout captcha après 30s, tentative quand même")
            time.sleep(2)

        # Cliquer sur Suivant
        submit_button = driver.find_element(By.ID, "idToken3_0")
        driver.execute_script("arguments[0].click();", submit_button)
        logger.info("✅ Formulaire email soumis")

        # Attendre que la page suivante charge (champ password)
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "idToken2")))
        except TimeoutException:
            time.sleep(3)  # Fallback
        return True

    except Exception as e:
        logger.error(f"❌ Erreur login étape 1: {e}")
        return False


def login_step2_password(driver: webdriver.Chrome, password: str) -> bool:
    """Deuxième étape de login : saisie du mot de passe"""
    try:
        wait = WebDriverWait(driver, 10)

        # Attendre le champ mot de passe
        password_field = wait.until(EC.presence_of_element_located((By.ID, "idToken2")))
        password_field.clear()
        password_field.send_keys(password)
        logger.info("✅ Mot de passe saisi")

        # Cliquer sur Connexion
        submit_button = driver.find_element(By.ID, "idToken4_0")
        driver.execute_script("arguments[0].click();", submit_button)
        logger.info("✅ Connexion en cours...")

        # Attendre que la page post-login charge (présence de boutons)
        try:
            WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
        except TimeoutException:
            time.sleep(5)  # Fallback
        return True

    except Exception as e:
        logger.error(f"❌ Erreur login étape 2: {e}")
        return False


def navigate_to_consumption(driver: webdriver.Chrome) -> bool:  # noqa: C901
    """Navigue vers la page 'Suivre ma consommation'"""
    try:
        # Accepter le 3ème popup cookies post-connexion
        accept_cookies(driver)

        # Cliquer sur le menu "Ma consommation"
        menu_buttons = driver.find_elements(By.TAG_NAME, "button")

        for btn in menu_buttons:
            if btn.is_displayed() and "Ma consommation" in btn.text:
                logger.info("🔍 Bouton 'Ma consommation' trouvé")
                driver.execute_script("arguments[0].click();", btn)
                # Attendre que les liens apparaissent
                try:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
                except TimeoutException:
                    time.sleep(2)  # Fallback
                break

        # Cliquer sur "Suivre ma consommation"
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            if link.is_displayed() and "Suivre ma consommation" in link.text:
                logger.info("🔍 Lien 'Suivre ma consommation' trouvé")
                driver.execute_script("arguments[0].click();", link)
                # Attendre que l'iframe apparaisse
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
                except TimeoutException:
                    time.sleep(3)  # Fallback
                break

        logger.info("✅ Navigation vers page de consommation réussie")
        return True

    except Exception as e:
        logger.error(f"❌ Erreur navigation: {e}")
        return False


def switch_to_iframe(driver: webdriver.Chrome) -> bool:
    """Bascule vers l'iframe contenant les mesures"""
    try:
        # Attendre que l'iframe voulue apparaisse (jusqu'à 20s)
        try:
            WebDriverWait(driver, 20).until(
                lambda d: any(
                    (
                        iframe.get_attribute("src")
                        and (
                            "mes-mesures" in iframe.get_attribute("src") or "donnees-de-mesures" in iframe.get_attribute("src")
                        )
                    )
                    for iframe in d.find_elements(By.TAG_NAME, "iframe")
                )
            )
        except TimeoutException:
            logger.warning("⚠️ Iframe des mesures non trouvée (timeout)")
            return False

        # Chercher l'iframe avec "mes-mesures" ou "donnees-de-mesures"
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            src = iframe.get_attribute("src") or ""
            if "mes-mesures" in src or "donnees-de-mesures" in src:
                driver.switch_to.frame(iframe)
                logger.info("✅ Basculé vers iframe des mesures")

                # Attendre que le DOM de l'iframe soit complètement chargé
                WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

                # Attendre que le contenu Angular soit chargé (bouton Heures dispo)
                try:
                    WebDriverWait(driver, 8).until(
                        lambda d: any(
                            span.is_displayed() and span.text.strip() == "Heures"
                            for span in d.find_elements(By.XPATH, "//span[contains(text(), 'Heures')]")
                        )
                    )
                    logger.info("⏳ Contenu iframe chargé")
                except TimeoutException:
                    time.sleep(5)  # Fallback
                    logger.info("⏳ Attente chargement contenu iframe...")

                return True

        logger.warning("⚠️ Iframe des mesures non trouvée (après attente)")
        return False

    except Exception as e:
        logger.error(f"❌ Erreur basculement iframe: {e}")
        return False


def select_heures_mode(driver: webdriver.Chrome) -> bool:
    """Sélectionne le mode 'Heures'"""
    try:
        # Chercher le span contenant "Heures"
        spans = driver.find_elements(By.XPATH, "//span[contains(text(), 'Heures')]")

        for span in spans:
            if span.is_displayed() and span.text.strip() == "Heures":
                # Remonter au label parent
                label = span.find_element(By.XPATH, "..")
                driver.execute_script("arguments[0].click();", label)
                logger.info("✅ Mode 'Heures' sélectionné")
                # Attendre que le calendrier soit prêt
                try:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Ouvrir le calendrier']"))
                    )
                except TimeoutException:
                    time.sleep(2)  # Fallback
                return True

        logger.warning("⚠️ Bouton 'Heures' non trouvé")
        return False

    except Exception as e:
        logger.error(f"❌ Erreur sélection mode Heures: {e}")
        return False


def select_date_range(driver: webdriver.Chrome, start_date: datetime, end_date: datetime) -> bool:  # noqa: C901
    """Sélectionne la plage de dates via le calendrier"""
    try:
        logger.info(f"🎯 Sélection période: {start_date.strftime('%d/%m/%Y')} → {end_date.strftime('%d/%m/%Y')}")

        # Trouver et cliquer sur le bouton calendrier
        calendar_button = None
        try:
            calendar_button = driver.find_element(By.XPATH, "//button[@aria-label='Ouvrir le calendrier']")
        except Exception:
            try:
                icon_element = driver.find_element(By.CSS_SELECTOR, "lnc-icon[icon='calendar_today']")
                calendar_button = icon_element.find_element(By.TAG_NAME, "button")
            except Exception:
                logger.error("❌ Bouton calendrier non trouvé")
                return False

        if calendar_button:
            driver.execute_script("arguments[0].click();", calendar_button)
            logger.info("✅ Calendrier ouvert")
            # Attendre que le calendrier soit chargé (boutons visibles)
            try:
                WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
            except TimeoutException:
                time.sleep(3)  # Fallback

        # Fonction pour sélectionner une date (année → mois → jour)
        def select_single_date(target_date: datetime, label: str) -> bool:
            try:
                logger.info(f"   📅 Sélection {label}: {target_date.strftime('%d/%m/%Y')}")

                # Étape 1: Cliquer sur bouton mois/année
                month_year_buttons = driver.find_elements(By.TAG_NAME, "button")
                for btn in month_year_buttons:
                    if btn.is_displayed():
                        aria_label = btn.get_attribute("aria-label") or ""
                        if "2025" in aria_label or "2024" in aria_label:
                            driver.execute_script("arguments[0].click();", btn)
                            # Attendre que les années soient visibles
                            try:
                                WebDriverWait(driver, 2).until(
                                    lambda d: any(
                                        b.is_displayed() and b.text.strip() == str(target_date.year)
                                        for b in d.find_elements(By.TAG_NAME, "button")
                                    )
                                )
                            except TimeoutException:
                                time.sleep(1)  # Fallback
                            logger.info("   1️⃣ Vue années ouverte")
                            break

                # Étape 2: Sélectionner l'année
                year_buttons = driver.find_elements(By.TAG_NAME, "button")
                for btn in year_buttons:
                    if btn.is_displayed() and btn.text.strip() == str(target_date.year):
                        driver.execute_script("arguments[0].click();", btn)
                        # Attendre que les mois soient visibles
                        try:
                            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
                        except TimeoutException:
                            time.sleep(1)  # Fallback
                        logger.info(f"   2️⃣ Année sélectionnée: {target_date.year}")
                        break

                # Étape 3: Sélectionner le mois
                month_names = [
                    "JAN",
                    "FÉV",
                    "MARS",
                    "AVR",
                    "MAI",
                    "JUIN",
                    "JUIL",
                    "AOÛT",
                    "SEPT",
                    "OCT",
                    "NOV",
                    "DÉC",
                ]
                target_month = month_names[target_date.month - 1]

                month_buttons = driver.find_elements(By.TAG_NAME, "button")
                for btn in month_buttons:
                    if btn.is_displayed() and target_month in btn.text.strip().upper():
                        driver.execute_script("arguments[0].click();", btn)
                        # Attendre que les jours soient chargés (IMPORTANT!)
                        try:
                            WebDriverWait(driver, 3).until(
                                lambda d: len(d.find_elements(By.CSS_SELECTOR, "td.days button")) > 0
                            )
                        except TimeoutException:
                            time.sleep(1)  # Fallback
                        logger.info(f"   3️⃣ Mois sélectionné: {target_month}")
                        break

                # Étape 4: Sélectionner le jour
                date_cells = driver.find_elements(By.CSS_SELECTOR, "td.days")
                for cell in date_cells:
                    try:
                        btn = cell.find_element(By.TAG_NAME, "button")
                        if btn.is_displayed():
                            spans = btn.find_elements(By.CSS_SELECTOR, "span.button-content")
                            btn_text = spans[0].text.strip() if spans else btn.text.strip()

                            if btn_text == str(target_date.day) or btn_text == f"{target_date.day:02d}":
                                driver.execute_script("arguments[0].click();", btn)
                                # Courte pause pour que le calendrier enregistre la sélection
                                try:
                                    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
                                except TimeoutException:
                                    time.sleep(1)  # Fallback
                                logger.info(f"   4️⃣ Jour sélectionné: {target_date.day}")
                                return True
                    except Exception:
                        pass

                logger.warning(f"   ⚠️ Jour {target_date.day} non trouvé")
                return False

            except Exception as e:
                logger.error(f"   ❌ Erreur sélection {label}: {e}")
                return False

        # Sélectionner date de début puis date de fin
        if not select_single_date(start_date, "date début"):
            return False

        if not select_single_date(end_date, "date fin"):
            return False

        logger.info("✅ Période sélectionnée avec succès")
        return True

    except Exception as e:
        logger.error(f"❌ Erreur sélection période: {e}")
        return False


def visualize_and_download(driver: webdriver.Chrome) -> bool:
    """Clique sur Visualiser puis Télécharger"""
    try:
        # Cliquer sur Visualiser
        visualiser_btn = None
        buttons = driver.find_elements(By.TAG_NAME, "button")

        for btn in buttons:
            if btn.is_displayed() and "visualiser" in btn.text.lower():
                visualiser_btn = btn
                break

        if not visualiser_btn:
            logger.error("❌ Bouton 'Visualiser' non trouvé")
            return False

        driver.execute_script("arguments[0].click();", visualiser_btn)
        logger.info("✅ Visualisation lancée")

        # Attendre que le bouton Télécharger soit cliquable (données chargées)
        try:
            WebDriverWait(driver, 10).until(
                lambda d: any(
                    btn.is_displayed() and "télécharger" in btn.text.lower() and btn.is_enabled()
                    for btn in d.find_elements(By.TAG_NAME, "button")
                )
            )
        except TimeoutException:
            time.sleep(8)  # Fallback

        # Cliquer sur Télécharger
        buttons = driver.find_elements(By.TAG_NAME, "button")

        for btn in buttons:
            if btn.is_displayed() and "télécharger" in btn.text.lower() and btn.is_enabled():
                driver.execute_script("arguments[0].click();", btn)
                logger.info("✅ Téléchargement lancé")
                time.sleep(3)  # Pause pour le téléchargement
                return True

        logger.warning("⚠️ Bouton 'Télécharger' non trouvé ou désactivé")
        return False

    except Exception as e:
        logger.error(f"❌ Erreur visualisation/téléchargement: {e}")
        return False


def split_date_range(start_date: datetime, end_date: datetime, max_days: int = 7) -> list:
    """
    Découpe une période en sous-périodes de max_days jours maximum

    Args:
        start_date: Date de début
        end_date: Date de fin
        max_days: Nombre maximum de jours par période (défaut: 7)

    Returns:
        Liste de tuples (start, end) pour chaque sous-période
    """
    periods = []
    current_start = start_date

    while current_start <= end_date:
        # Calculer la date de fin pour cette période
        current_end = min(current_start + timedelta(days=max_days - 1), end_date)
        periods.append((current_start, current_end))

        # Passer à la période suivante
        current_start = current_end + timedelta(days=1)

    return periods


def download_consumption_data(  # noqa: C901
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    headless: bool = False,
) -> bool:
    """
    Télécharge les données de consommation pour la période spécifiée.
    Découpe automatiquement en périodes de 7 jours si nécessaire.

    Args:
        start_date (Optional[datetime]): Date de début (par défaut: J-7)
        end_date (Optional[datetime]): Date de fin (par défaut: hier)
        headless (bool): Mode sans interface graphique (défaut: False = visible)

    Returns:
        bool: True si succès complet, False si au moins une erreur

    Raises:
        ValueError: Si les dates sont invalides
    """

    # Supprimer les warnings de subprocess (termination des processus)
    warnings.filterwarnings("ignore", category=ResourceWarning)
    warnings.filterwarnings("ignore", message=".*subprocess.*")

    # Validation et normalisation des dates
    try:
        start_date, end_date = validate_date_range(start_date, end_date)
    except ValueError as e:
        logger.error(f"❌ Dates invalides: {e}")
        return False

    # Découper la période en sous-périodes de 7 jours maximum
    periods = split_date_range(start_date, end_date, max_days=7)

    total_days = (end_date - start_date).days + 1
    logger.info(f"🚀 Démarrage du téléchargement: {start_date.strftime('%d/%m/%Y')} → {end_date.strftime('%d/%m/%Y')}")
    logger.info(f"📊 Période totale: {total_days} jours - Découpage en {len(periods)} période(s) de 7 jours max")

    driver = None
    success_count = 0
    error_count = 0

    try:
        # 1. Initialiser le driver UNE SEULE FOIS avec le mode headless
        driver = setup_driver(headless=headless)

        # 2. Accéder à la page
        driver.get(BASE_URL)
        logger.info(f"📍 Page chargée: {BASE_URL}")

        # Attendre que la page soit chargée (présence du bouton cookies ou formulaire)
        try:
            WebDriverWait(driver, 5).until(
                lambda d: d.find_element(By.ID, "popin_tc_privacy_button_3") or d.find_element(By.ID, "idToken1")
            )
        except TimeoutException:
            time.sleep(3)  # Fallback

        # 3. Accepter les cookies
        accept_cookies(driver)
        time.sleep(1)  # Courte pause après fermeture cookies

        # 4. Login étape 1 (email)
        if not login_step1_email(driver, EMAIL):
            return False

        # 5. Login étape 2 (password)
        if not login_step2_password(driver, PASSWORD):
            return False

        # 6. Accepter cookies post-login et naviguer
        if not navigate_to_consumption(driver):
            return False

        # 7. Basculer vers l'iframe
        if not switch_to_iframe(driver):
            return False

        # 8. Sélectionner mode Heures
        if not select_heures_mode(driver):
            return False

        # 9. BOUCLE SUR CHAQUE PÉRIODE DE 7 JOURS
        for i, (period_start, period_end) in enumerate(periods, 1):
            logger.info(f"\n{'='*70}")
            logger.info(
                f"📥 PÉRIODE {i}/{len(periods)}: {period_start.strftime('%d/%m/%Y')} → {period_end.strftime('%d/%m/%Y')}"
            )
            logger.info(f"{'='*70}")

            try:
                # Sélectionner la période dans le calendrier
                if not select_date_range(driver, period_start, period_end):
                    logger.error(f"❌ Échec sélection période {i}")
                    error_count += 1
                    continue

                # Visualiser et télécharger
                if not visualize_and_download(driver):
                    logger.error(f"❌ Échec téléchargement période {i}")
                    error_count += 1
                    continue

                success_count += 1
                logger.info(f"✅ Période {i}/{len(periods)} téléchargée avec succès")

                # Petite pause entre chaque téléchargement
                if i < len(periods):
                    time.sleep(1)  # Pause réduite entre périodes

            except Exception as e:
                logger.error(f"❌ Erreur période {i}: {e}")
                error_count += 1
                continue

        # 10. Résumé final
        logger.info("\n" + "=" * 70)
        logger.info("📊 RÉSUMÉ")
        logger.info("=" * 70)
        logger.info(f"✅ Succès: {success_count}/{len(periods)} périodes")
        logger.info(f"❌ Erreurs: {error_count}/{len(periods)} périodes")

        if error_count == 0:
            logger.info("🎉 Téléchargement complet terminé avec succès!")
            return True
        elif success_count > 0:
            logger.warning("⚠️ Téléchargement partiel - certaines périodes ont échoué")
            return False
        else:
            logger.error("❌ Échec complet - aucune période téléchargée")
            return False

    except Exception as e:
        logger.error(f"❌ Erreur générale: {type(e).__name__}")
        logger.debug(f"Détails: {str(e)}")  # Détails seulement en mode debug
        # Ne PAS afficher le traceback complet en production (risque de fuite d'info)
        return False

    finally:
        if driver:
            try:
                # Fermeture propre du navigateur sans logs d'erreur
                import logging

                # Désactiver temporairement les logs de Selenium
                selenium_logger = logging.getLogger("selenium")
                original_level = selenium_logger.level
                selenium_logger.setLevel(logging.CRITICAL)

                try:
                    # Fermer toutes les fenêtres
                    if driver.window_handles:
                        driver.close()
                    time.sleep(0.3)
                except Exception:
                    pass

                try:
                    # Terminer le driver et le processus
                    driver.quit()
                except Exception:
                    pass

                try:
                    # Forcer la fermeture du service si encore actif
                    if hasattr(driver, "service") and driver.service.process:
                        if driver.service.process.poll() is None:
                            driver.service.process.kill()
                except Exception:
                    pass

                # Restaurer le niveau de log
                selenium_logger.setLevel(original_level)

                logger.info("✅ Navigateur fermé proprement")

            except Exception:
                # Ignorer toutes les erreurs de fermeture
                logger.info("✅ Navigateur fermé")


def main():
    """Point d'entrée principal"""
    import argparse

    parser = argparse.ArgumentParser(description="Téléchargeur automatique de données Enedis")
    parser.add_argument("--start-date", type=str, help="Date de début (format: DD/MM/YYYY)")
    parser.add_argument("--end-date", type=str, help="Date de fin (format: DD/MM/YYYY)")
    parser.add_argument("--loop", action="store_true", help="Mode boucle (toutes les 30 min)")
    parser.add_argument("--interval", type=int, default=30, help="Intervalle en minutes (défaut: 30)")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Mode sans interface (navigateur invisible)",
    )

    args = parser.parse_args()

    # Parser les dates si fournies
    start_date = None
    end_date = None

    if args.start_date:
        start_date = datetime.strptime(args.start_date, "%d/%m/%Y")
    if args.end_date:
        end_date = datetime.strptime(args.end_date, "%d/%m/%Y")

    # Mode normal (une seule exécution)
    if not args.loop:
        success = download_consumption_data(start_date, end_date, headless=args.headless)
        sys.exit(0 if success else 1)

    # Mode boucle
    logger.info(f"🔄 Mode boucle activé (intervalle: {args.interval} minutes)")

    while True:
        try:
            logger.info(f"\n{'='*70}")
            logger.info(f"🕐 Exécution: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"{'='*70}\n")

            download_consumption_data(start_date, end_date, headless=args.headless)

            logger.info(f"\n⏰ Prochaine exécution dans {args.interval} minutes...")
            time.sleep(args.interval * 60)

        except KeyboardInterrupt:
            logger.info("\n🛑 Arrêt demandé par l'utilisateur")
            break
        except Exception as e:
            logger.error(f"❌ Erreur dans la boucle: {e}")
            logger.info(f"⏰ Nouvelle tentative dans {args.interval} minutes...")
            time.sleep(args.interval * 60)


if __name__ == "__main__":
    main()
