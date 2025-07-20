import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import select
from sqlalchemy.orm import Session

from server.database.models.actor import Actor
from server.scraper.tmdb_scraper import TmdbScraper

scraper = TmdbScraper()
scraper.scrape(searched_film="Blade runner 2049")
scraper.close()

# result = Utils.get_actor(name="Tos", surname="Hanks")

# u = Utils.create_actor(name="FfffFF", surname="RRR")
# print(type(u))


# connector = Connector()
# session = Session(connector.engine)
# scraper = TmdbScraper(url="https://www.themoviedb.org/")
# film = scraper.scrape(searched_film="Blade runner 2049")
# scraper.close()


# # for card in cards:
# #   element = card.find_element(By.TAG_NAME, "h2")


# driver.quit()
