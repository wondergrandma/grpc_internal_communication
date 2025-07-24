from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# TMDB SCRAPER VARIABLES
IMAGE_STORAGE_DIRECTORY=getenv("IMAGE_STORAGE_DIRECTORY")
