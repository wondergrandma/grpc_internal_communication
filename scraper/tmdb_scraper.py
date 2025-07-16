from selenium.webdriver.chrome.options import Options
import requests
from scraper.scraper_base import ScraperBase
from selenium.webdriver.support.ui import WebDriverWait
from scraper.dto import ScrapedFilm
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import re
from typing import List, Tuple
from selenium.webdriver.remote.webelement import WebElement
from database.models.actor import Actor
from scraper.utils import Utils

class TmdbScraper(ScraperBase):
    def __init__(self, url):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 10)

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
        #age_restriction = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/div/span[1]')))
        length = self.extract_time(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/div/span[4]'))))
        overview = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[3]/div/p')))
        actors = self.extract_actors(element=self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="cast_scroller"]/ol'))))

        s=self.get_actors(actors)
        for ss in s: 
            print(f"{ss.Name} {ss.Surname}")

        Utils.create_film(name=title.text, make_year=self.extract_year(make_year.text), hour=length[0], minute=length[1], 
                           categories="", overview=overview.text, 
                           actors=self.get_actors(actors), director="", writer="", rating="", cover_path="")

        return ScrapedFilm(Name=title.text, MakeYear=self.extract_year(make_year.text), Hour=length[0], Minute=length[1], 
                           Categories="", Overview=overview.text, 
                           Actors=self.get_actors(actors), Director="", Writer="", Rating="", CoverPath="")
    
    def get_actors(self, actors: List[str]) -> List[Actor]:
        actors_list: List[Actor] = []

        for actor in actors:
            actor_name = self.extract_name_surname(actor)
            temp_actor: Actor = Utils.get_actor(name=actor_name[0], surname=actor_name[1])

            if(isinstance(temp_actor, Actor)):
                actors_list.append(temp_actor)
            else:
                created: bool = Utils.create_actor()

                if created:
                    new_actor: Actor = Utils.get_actor(name=actor_name[0], surname=actor_name[1])
                    actors_list.append(new_actor)
        
        return actors_list
            
    def extract_year(self, date: str):
        split_date: List[str] = date.split("/")
        year: int = int(split_date[2])

        return year

    def extract_time(self, element: WebElement) -> Tuple[int, int]:
        try:
            split: list = element.text.split(" ")
            hours: int = int(re.match(r"^\d+", split[0].strip()).group(0))
            minutes: int = int(re.match(r"^\d+", split[1].strip()).group(0))

            return hours, minutes
        except Exception as e:
            raise

    def extract_actors(self, element: WebElement) -> List[str]:
        try:
            actors_card = element.find_elements(By.CLASS_NAME, 'card')
            actors = []

            for i in range(4):
                temp_actor = actors_card[i].find_element(By.XPATH, f'//*[@id="cast_scroller"]/ol/li[{i+1}]/p[1]/a')
                actors.append(temp_actor.text)
            
            return actors
        except Exception as e:
            raise
    
    def extract_name_surname(self, actor: str) -> Tuple[str, str]:
        try:
            split_actor_name: List[str] = actor.split(" ")
            name_length: int = len(split_actor_name)
            name: str
            surname: str

            for name in split_actor_name:
                if(name_length == 2):
                    name = split_actor_name[0]
                    surname = split_actor_name[1]
                else:
                    name = split_actor_name[0]
                    surname = " ".join(split_actor_name[1:name_length])

            return name, surname
        
        except Exception as e:
            raise
    
    def close(self):
        self.driver.quit()