from selenium.webdriver.chrome.options import Options
import requests
from scraper_base import ScraperBase
from selenium.webdriver.support.ui import WebDriverWait
from dto import ScrapedFilm
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import re


class TmdbScraper(ScraperBase):
    def __init__(self, url):
        self.url = url
        #options = Options()
        #options.add_argument('--headless')
        #self.driver = webdriver.Chrome(options=options)
        self.driver = webdriver.Chrome()
        wait = WebDriverWait(self.driver, 10)

    def check_site_availability(self) -> bool:
        try: 
            status: bool = requests.get(self.url).ok
            return status
        except:
            # TODO: Logger
            return False
    
    def scrape(self, searched_film: str) -> ScrapedFilm | bool:
        search = self.driver.find_element(By.ID, "inner_search_v4")
        search.send_keys(searched_film)
        search.send_keys(Keys.RETURN)
        cards = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.card.v4.tight')))

        cards[0].find_element(By.TAG_NAME, "a").click()

        title = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/h2/a')))
        make_year = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/div/span[2]')))
        age_restriction = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/div/span[1]')))
        length = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/div/span[4]')))
        overview = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[3]/div/p')))

        print(re.match(r"^\s*\d+[h]\s*\d+[m]", length))

        return ScrapedFilm(title=title, make_year=make_year, age_restriction=age_restriction, length=length, overview=overview)
