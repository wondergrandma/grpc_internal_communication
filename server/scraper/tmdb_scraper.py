import glob
import logging
import os
import re
from types import SimpleNamespace
from typing import List, Tuple
from urllib.request import urlretrieve

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy.engine.row import Row

from server import IMAGE_STORAGE_DIRECTORY
from server.database.models.actor import Actor
from server.database.models.category import Category
from server.database.models.director import Director
from server.database.queries.actor_queries import ActorQuery
from server.database.queries.category_queries import CategoryQuery
from server.database.queries.director_queries import DirectorQuery
from server.database.queries.film_queries import FilmQuery
from server.scraper.dto import ScrapedFilm
from server.scraper.scraper_base import ScraperBase


class TmdbScraper(ScraperBase):
    def __init__(self):
        url: str = "https://www.themoviedb.org/"
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 10)
        self.logger = logging.getLogger(__name__)

    def check_site_availability(self) -> bool:
        try:
            status: bool = requests.get(self.url).ok
            return status
        except:
            # TODO: Logger
            return False

    def search_film(self, searched_film):
        self.logger.info(msg=f"Searching for {searched_film}.")

        search = self.driver.find_element(By.ID, "inner_search_v4")
        search.send_keys(searched_film)
        search.send_keys(Keys.RETURN)
        cards_element = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.v4.tight"))
        )

        cards_element[0].find_element(By.TAG_NAME, "a").click()

    def scrape(self, searched_film: str) -> int:
        self.search_film(searched_film)

        self.logger.info(msg=f"Scraping {searched_film}.")

        # TODO: Find way how to convert age restrictions from different countries to one format
        age_restriction: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "certification"))
        )

        time: Tuple[int, int] = self.extract_time(self._get_time())

        new_film: int = FilmQuery.create_film(
            name=self._get_title_element().text,
            make_year=self.extract_year(self._get_make_year_element()),
            hour=time[0],
            minute=time[1],
            categories=self.get_categories(self._get_genre()),
            overview=self._get_overview().text,
            actors=self.get_actors(self._get_actors_element()),
            directors=self.get_directors(self._get_directors_element()),
            rating=self.extract_rating(self._get_rating()),
            cover_path=self.store_cover_image(self._get_cover_image()),
        )

        return new_film

    def _get_title_element(self) -> WebElement:
        title_element: WebElement = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/h2/a')
            )
        )

        return title_element

    def _get_make_year_element(self) -> WebElement:
        make_year_element: WebElement = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="original_header"]/div[2]/section/div[1]/div/span[2]',
                )
            )
        )

        return make_year_element

    def _get_time(self):
        length_element: WebElement = self.extract_time(
            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="original_header"]/div[2]/section/div[1]/div/span[4]',
                    )
                )
            )
        )

        return length_element

    def _get_genre(self) -> WebElement:
        genre_element: WebElement = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]',
                )
            )
        )
        return genre_element

    def _get_overview(self) -> WebElement:
        overview_element: WebElement = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="original_header"]/div[2]/section/div[3]/div/p')
            )
        )

        return overview_element

    def _get_actors_element(self) -> WebElement:
        actors_element: WebElement = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cast_scroller"]/ol'))
        )

        return actors_element

    def _get_directors_element(self) -> WebElement:
        directors_element: WebElement = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="original_header"]/div[2]/section/div[3]/ol')
            )
        )

        return directors_element

    def _get_rating(self) -> WebElement:
        rating_element: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "percent"))
        )

        return rating_element

    def _get_cover_image(self) -> WebElement:
        cover_image_element: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "image_content"))
        )

        return cover_image_element

    def get_directors(self, directors: WebElement) -> List[Director]:
        directors_list: List[Director] = []

        try:
            extracted_directors: Tuple[str, str] = self.extract_director(directors)

            for director in extracted_directors:
                temp_director: Director = DirectorQuery.get_director_by_name(
                    name=director[0], surname=director[1]
                )

                if isinstance(temp_director, Director):
                    directors_list.append(temp_director)
                else:
                    created: Tuple[int] = DirectorQuery.create_director(
                        name=director[0], surname=director[1]
                    )

                    if isinstance(created, Row):
                        new_direcotr: Director = DirectorQuery.get_director_by_id(
                            created[0]
                        )
                        directors_list.append(new_direcotr)

            return directors_list
        except Exception as e:
            self.logger.error(msg=e, exc_info=True)
            return []

    def get_categories(self, categories: WebElement) -> List[Category]:
        categories_list: List[Category] = []

        try:
            extracted_categories: List[str] = self.extract_genre(categories)

            for genre in extracted_categories:
                temp_gener: Category = CategoryQuery.get_category_by_genre(genre)

                if isinstance(temp_gener, Category):
                    categories_list.append(temp_gener)
                else:
                    created: Tuple[int] = CategoryQuery.create_category(genre)

                    if isinstance(created, Row):
                        new_category: Category = CategoryQuery.get_category_by_id(
                            created[0]
                        )
                        categories_list.append(new_category)

            return categories_list
        except Exception as e:
            logging.error(msg=e, exc_info=True)
            return []

    def get_actors(self, actors: WebElement) -> List[Actor]:
        actors_list: List[Actor] = []

        try:
            extracted_actors: List[str] = self.extract_actors(actors)

            for actor in extracted_actors:
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
        except Exception as e:
            logging.error(msg=e, exc_info=True)
            return []

    def extract_director(self, people: WebElement) -> List[Tuple[str, str]]:
        directors: List[Tuple[str, str]] = []
        try:
            people_list: List[WebElement] = people.find_elements(By.TAG_NAME, "li")

            for people in people_list:
                name = people.find_element(By.TAG_NAME, "a")

                role = people.find_elements(By.TAG_NAME, "p")[1]

                temp_person: SimpleNamespace = SimpleNamespace(
                    name=name.text,
                    role=[r.strip().lower() for r in role.text.split(",")],
                )

                if "director" in temp_person.role:
                    name_surname: Tuple[str, str] = self.extract_name_surname(
                        temp_person.name
                    )
                    directors.append(name_surname)

            return directors
        except Exception:
            raise

    def extract_genre(self, genres: WebElement) -> List[str]:
        try:
            genre_elements: List[WebElement] = genres.find_elements(By.TAG_NAME, "a")
            geners_list: List[str] = []

            for gener in genre_elements:
                geners_list.append(gener.text)

            return geners_list
        except Exception:
            raise

    def extract_year(self, date: WebElement):
        split_date: List[str] = date.text.split("/")
        year: int = int(split_date[2].split(" ")[0])

        return year

    def extract_time(self, element: WebElement) -> Tuple[int, int]:
        try:
            split: list = element.text.split(" ")
            hours: int = int(re.match(r"^\d+", split[0].strip()).group(0))
            minutes: int = int(re.match(r"^\d+", split[1].strip()).group(0))

            return hours, minutes
        except Exception:
            raise

    def extract_actors(self, element: WebElement) -> List[str]:
        try:
            actors_card = element.find_elements(By.CLASS_NAME, "card")
            actors: List[str] = []

            for i in range(len(actors_card)):
                temp_actor = actors_card[i].find_element(
                    By.XPATH, f'//*[@id="cast_scroller"]/ol/li[{i+1}]/p[1]/a'
                )
                actors.append(temp_actor.text)

            return actors
        except Exception:
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

        except Exception:
            raise

    def extract_rating(self, rating_element: WebElement):
        percentage_element: WebElement = rating_element.find_element(
            By.TAG_NAME, "span"
        )
        percentage: str = percentage_element.get_attribute("class")
        extracted_number: int = int(percentage.split("-")[1].split("r")[1])

        return self.convert_to_star_rating(extracted_number)

    def convert_to_star_rating(self, percentage: int) -> int:
        star_rating: int = (percentage / 100) * 10
        return star_rating

    def store_cover_image(self, image_element: WebElement) -> str:
        img: WebElement = image_element.find_element(By.TAG_NAME, "img")
        srcset: str = img.get_attribute("srcset")
        split: str = srcset.split(",")[1].split(" ")
        image_number: int

        for s in split:
            if re.search(r"^https://.*(\.)([a-zA-Z]{3})", s) != None:
                cover_image_number: int = self.generate_cover_image_number()
                image_number = cover_image_number
                urlretrieve(
                    s, f"{IMAGE_STORAGE_DIRECTORY}/cover_image_{cover_image_number}.jpg"
                )

        return f"cover_image_{image_number}.jpg"

    # TODO: Create default image if no image is found
    def generate_cover_image_number(self) -> int:
        last_file_number: int = 0

        try:
            if last_file_number == 0:
                list_of_files: List[str] = glob.glob(f"{IMAGE_STORAGE_DIRECTORY}/*.jpg")
                last_created_file: str = max(list_of_files, key=os.path.getctime).split(
                    "/"
                )[-1]
                last_file_number: int = int(
                    re.match(r"^(cover_image_)(\d*)(\.jpg)$", last_created_file).group(
                        2
                    )
                )

            while os.path.exists(
                f"{IMAGE_STORAGE_DIRECTORY}/cover_image_{last_file_number}.jpg"
            ):
                last_file_number += 1

            return last_file_number
        except Exception:

            raise

    def close(self):
        self.driver.quit()
