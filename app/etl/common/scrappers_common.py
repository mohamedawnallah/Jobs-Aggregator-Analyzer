from abc import ABC, abstractmethod
from typing import Optional, Iterator, Any
from etl.models.country_model import Country

class CountriesScrapper(ABC):
    """Countries Scrapper"""
    @abstractmethod
    def get_countries(
        self, countries_no: Optional[int] = None
    ) -> Iterator[Country]:
        """Get the list of countries supported by indedd"""

class PagesNoScrapper(ABC):
    """Pages No Scrapper"""
    @abstractmethod
    def is_last_page(self, *args, **kwargs) -> int:
        """Get the number of pages for a given country"""


class JobsCountriesScrapper(ABC):
    """Jobs Countries Scrapper"""
    @abstractmethod
    def get_jobs_countries(
        self, countries_input: Iterator[Country], job_title: str, page_no: Optional[int] = None
    ) -> Any:
        """Gets Jobs for all available countries based on the given job title also the page number if available"""

