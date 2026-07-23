from pathlib import Path
import os

from dotenv import load_dotenv


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()


# ==========================================================
# PROJECT ROOT DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent


# ==========================================================
# DATA DIRECTORY
# ==========================================================

DATA_DIR = BASE_DIR / "data"

RESULT_HISTORY_FILE = (
    DATA_DIR / "result_history.json"
)

LATEST_RESULTS_FILE = (
    DATA_DIR / "latest_results.json"
)


# ==========================================================
# WEBSITE DIRECTORY
# ==========================================================

WEBSITE_DIR = BASE_DIR / "docs"

INDEX_FILE = WEBSITE_DIR / "index.html"

STYLE_FILE = WEBSITE_DIR / "style.css"

# ==========================================================
# SPPU RESULT DASHBOARD
# ==========================================================

RESULT_DASHBOARD_URL = (
    "https://onlineresults.unipune.ac.in/Result/Dashboard/Default"
)


# ==========================================================
# WEBSITE CONFIGURATION
# ==========================================================

WEBSITE_NAME = os.getenv(
    "WEBSITE_NAME",
    "SPPU Result Monitor"
)


# ==========================================================
# EMAIL CONFIGURATION
# ==========================================================

EMAIL_ADDRESS = os.getenv(
    "EMAIL_ADDRESS"
)

EMAIL_APP_PASSWORD = os.getenv(
    "EMAIL_APP_PASSWORD"
)

NOTIFICATION_EMAIL = os.getenv(
    "NOTIFICATION_EMAIL"
)


# ==========================================================
# REQUEST CONFIGURATION
# ==========================================================

REQUEST_TIMEOUT = 30