from __future__ import annotations
from abc import ABC, abstractmethod

class ScraperBase(ABC):

    @abstractmethod
    def check_site_availability(self) -> bool:
        pass

    @abstractmethod
    def scrape(self) -> bool:
        pass