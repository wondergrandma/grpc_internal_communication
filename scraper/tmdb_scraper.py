import re
from typing import List, Tuple

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy.engine.row import Row

from database.models.actor import Actor
from database.models.category import Category
from database.queries.actor_queries import ActorQuery
from database.queries.category_queries import CategoryQuery
from database.queries.film_queries import FilmQuery
from scraper.dto import ScrapedFilm
from scraper.scraper_base import ScraperBase


class TmdbScraper(ScraperBase):
    def __init__(self, url):
        options = Options()
        options.add_argument("--headless")
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

    # TODO: Check naming of variables -> length, actors
    def scrape(self, searched_film: str) -> ScrapedFilm | bool:
        search = self.driver.find_element(By.ID, "inner_search_v4")
        search.send_keys(searched_film)
        search.send_keys(Keys.RETURN)
        cards_element = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.v4.tight"))
        )

        cards_element[0].find_element(By.TAG_NAME, "a").click()

        title_element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/h2/a')
            )
        )
        make_year_element = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="original_header"]/div[2]/section/div[1]/div/span[2]',
                )
            )
        )
        age_restriction = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="original_header"]/div[2]/section/div[1]/div/span[1]',
                )
            )
        )
        length_element = self.extract_time(
            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="original_header"]/div[2]/section/div[1]/div/span[4]',
                    )
                )
            )
        )
        genre_element = self.extract_genre(
            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]',
                    )
                )
            )
        )
        overview_element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="original_header"]/div[2]/section/div[3]/div/p')
            )
        )
        actors_element = self.extract_actors(
            element=self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="cast_scroller"]/ol')
                )
            )
        )

        new_film: int = FilmQuery.create_film(
            name=title_element.text,
            make_year=self.extract_year(make_year_element.text),
            hour=length_element[0],
            minute=length_element[1],
            categories=self.get_categories(genre_element),
            overview=overview_element.text,
            actors=self.get_actors(actors_element),
            director="",
            writer="",
            rating=1,
            cover_path="",
        )

        return new_film

    def get_categories(self, categories: List[str]) -> List[Category]:
        categories_list: List[Category] = []

        for genre in categories:
            temp_gener: Category = CategoryQuery.get_category_by_genre(genre)

            if isinstance(temp_gener, Category):
                categories_list.append(temp_gener)
            else:
                created: Tuple[int] = CategoryQuery.create_category(genre)

                if isinstance(created, Row):
                    print("SOM TU")
                    new_category: Category = CategoryQuery.get_category_by_id(
                        created[0]
                    )
                    categories_list.append(new_category)

        return categories_list

    def get_actors(self, actors: List[str]) -> List[Actor]:
        actors_list: List[Actor] = []

        for actor in actors:
            actor_name = self.extract_name_surname(actor)
            temp_actor: Actor = ActorQuery.get_actor_by_name(
                name=actor_name[0], surname=actor_name[1]
            )

            if isinstance(temp_actor, Actor):
                actors_list.append(temp_actor)
            else:
                created: Tuple[int] = ActorQuery.create_actor(
                    name=actor_name[0], surname=actor_name[1]
                )

                if isinstance(created, Row):
                    new_actor: Actor = ActorQuery.get_actor_by_id(created[0])
                    actors_list.append(new_actor)

        return actors_list

    def extract_genre(self, genres: WebElement) -> List[str]:
        genre_elements: List[WebElement] = genres.find_elements(By.TAG_NAME, "a")
        geners_list: List[str] = []

        for gener in genre_elements:
            geners_list.append(gener.text)

        return geners_list

    def extract_year(self, date: str):
        split_date: List[str] = date.split("/")
        year: int = int(split_date[2].split(" ")[0])

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
            actors_card = element.find_elements(By.CLASS_NAME, "card")
            actors = []

            for i in range(4):
                temp_actor = actors_card[i].find_element(
                    By.XPATH, f'//*[@id="cast_scroller"]/ol/li[{i+1}]/p[1]/a'
                )
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
                if name_length == 2:
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
