import logging
import logging.handlers
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# LOGGER SETTINGS
LOGGING_DIRECTORY = os.getenv("LOGGING_DIRECTORY")
LOGGING_FILE = os.getenv("LOGGING_FILE")
FORMAT = os.getenv("FORMAT")
LOG_LEVEL = os.getenv("LOG_LEVEL")

# TMDB SCRAPER VARIABLES
IMAGE_STORAGE_DIRECTORY = os.getenv("IMAGE_STORAGE_DIRECTORY")


if not (os.path.exists(LOGGING_DIRECTORY)):
    os.makedirs(name=LOGGING_DIRECTORY, exist_ok=True)

log_level_dict = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

logger = logging.getLogger(__name__)
handler = logging.handlers.RotatingFileHandler(
    filename=f"{LOGGING_DIRECTORY}/{LOGGING_FILE}",
    encoding="utf-8",
    mode="a",
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
)
logging.basicConfig(
    format=FORMAT,
    level=log_level_dict.get(LOG_LEVEL, logging.INFO), handlers=[handler]
)
