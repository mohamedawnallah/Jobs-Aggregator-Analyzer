import pytest
from etl.scrappers.indeed_scrapper import IndeedScrapper
from etl.scrappers.data_stack_jobs_scraper import DataStackJobsScraper
from etl.utils.utils import Utils
from etl.utils.job_specifications import OrSpecification,ProgrammingLanguagesSpecification,IngestTechSpecification, BachelorComputerScienceSpecification

@pytest.fixture
def configs() -> dict:
    """Fixture for configs"""
    configs: dict = Utils.get_configs("app/etl/settings/configs.toml")
    return configs

@pytest.fixture
def job_specifications(configs: dict) -> dict:
    """Fixture for job_specifications"""
    job_specfications = ProgrammingLanguagesSpecification(configs) | IngestTechSpecification(configs) | BachelorComputerScienceSpecification(configs)
    return job_specfications

@pytest.fixture
def indeed_scrapper(configs: dict, job_specifications: OrSpecification) -> "IndeedScrapper":
    """Fixture for IndeedScrapper"""
    indeed_scrapper: IndeedScrapper = IndeedScrapper(configs,job_specifications)
    return indeed_scrapper

@pytest.fixture()
def data_stack_jobs_scraper(configs: dict) -> DataStackJobsScraper:
    """Fixture for returning a DataStackJobsScraper object"""
    return DataStackJobsScraper(configs=configs)

@pytest.fixture
def get_html_tags(configs: dict) -> list:
    """Fixture for retrieving sample html for DataStackJobsScraper tests."""
    html_tags = configs['html_elements']['html_tags']
    return html_tags