from abc import abstractmethod, ABC
from typing import Optional, Iterator, Any
from etl.models.job_dataclasses import JobBasicInfo, CompanyBasicInfo, JobMoreInfo, JobFullInfo, Country
from etl.utils.job_specifications import BaseSpecification


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
    def get_pages_no(self, *args, **kwargs) -> int:
        """Get the number of pages for a given country"""


class JobsCountriesScrapper(ABC):
    """Jobs Countries Scrapper"""
    @abstractmethod
    def get_jobs_countries(
        self, countries_input: Iterator[Country], job_title: str, page_no: Optional[int] = None
    ) -> Any:
        """Gets Jobs for all available countries based on the given job title also the page number if available"""


class JobCompanyBasicInfoTransformer(ABC):
    """Basic Job Info Transformer Abstract Class for other Web Scrappers"""

    @staticmethod
    @abstractmethod
    def transform(job_basic_info: JobBasicInfo, company_basic_info: CompanyBasicInfo,**kwargs) -> tuple[JobBasicInfo,CompanyBasicInfo]:
        """Transform the basic job company info"""


class JobMoreInfoTransformer(ABC):
    """More Job Info Transformer Abstract Class for other Web Scrappers"""

    @staticmethod
    @abstractmethod
    def transform(job_info: JobMoreInfo,**kwargs) -> JobMoreInfo:
        """Transform the more job info"""


class JobSkillsTransformer(ABC):
    """Skills Transformer Abstract Class for other Web Scrappers"""

    @staticmethod
    @abstractmethod
    def transform(job_specifications: BaseSpecification, job_description: str) -> dict[str]:
        """Transform the skills"""


class JobPagesNoTransformer(ABC):
    """Pages Transformer Abstract Class for other Web Scrappers"""

    @staticmethod
    @abstractmethod
    def transform(*args, **kwargs) -> dict:
        """Transform the job info"""


class CountriesTransformer(ABC):
    """Countries Transformer"""

    @staticmethod
    @abstractmethod
    def transform(country_name: str, country_link: str) -> Country:
        """Transform the job info"""


class CSVPersistenceManager(ABC):
    """Persistence Manager Abstract Class for other Web Scrappers"""

    @staticmethod
    @abstractmethod
    def write_to_csv(
        csv_file_name: str,
        jobs: Any,
        *args,
        **kwargs
    ) -> int:
        """Save jobs depending on the website also the passed job title"""
        pass

class DBPersistenceManager(ABC):
    """Persistence Manager Abstract Class for other Web Scrappers"""

    @staticmethod
    @abstractmethod
    def write_to_db(
        db_file_name: str,
        jobs: Any
    ) -> int:
        """Save jobs depending on the website also the passed job title"""


class Extractor(ABC):
    """Extractor"""
    @abstractmethod
    def extract(self, *args, **kwargs) -> Any:
        """Extract data from Scrappers"""

class Transformer(ABC):
    """Transformer"""
    @abstractmethod
    def transform(self, *args, **kwargs) -> Any:
        """Transform data"""

class Loader(ABC):
    """Loader"""
    @abstractmethod
    def load(self, *args, **kwargs) -> Any:
        """Load data into one of the provided persistence managers"""

