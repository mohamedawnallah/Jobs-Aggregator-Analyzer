from abc import ABC, abstractmethod
from typing import Optional, Iterator, Any
from models.country_model import CountryDim

class CountriesScrapper(ABC):
    """Countries Scrapper"""
    @abstractmethod
    def get_countries(
        self, countries_no: Optional[int] = None
    ) -> Iterator[CountryDim]:
        """Get the list of countries supported by indedd"""

class PagesNoScrapper(ABC):
    """Pages No Scrapper"""
    @abstractmethod
    def is_last_page(self, *args, **kwargs) -> int:
        """Get the number of pages for a given country"""


class JobsScrapper(ABC):
    """Jobs Countries Scrapper"""
    @abstractmethod
    def get_jobs_in_country(
        self, countries: CountryDim, job_title: str, page_no: Optional[int] = None
    ) -> Any:
        """Gets Jobs for all available countries based on the given job title also the page number if available"""

    @abstractmethod
    def get_jobs_in_countries(
        self, countries: Iterator[CountryDim], job_title: str, page_no: Optional[int] = None
    ) -> Any:
        """Gets Jobs for all available countries based on the given job title also the page number if available"""
