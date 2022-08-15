import pytest
from etl.scrappers.indeed_scrapper import IndeedScrapper
from etl.scrappers.data_stack_jobs_scraper import DataStackJobsScraper
from etl.utils.utils import Utils
from etl.utils.job_specifications import OrSpecification,ProgrammingLanguagesSpecification,IngestTechSpecification, BachelorComputerScienceSpecification
from etl.apis.job_skills_api import JobSkillsAPI

@pytest.fixture(scope="session")
def etl_configs() -> dict:
    """Fixture for configs"""
    configs: dict = Utils.get_configs("app/etl/settings/etl_configs.yaml")
    return configs


@pytest.fixture(scope="session")
def job_skills(etl_configs: dict) -> str:
    """Fixture for job skills"""
    skills_api = JobSkillsAPI(etl_configs["data_sources"]["lightcast_skills"])
    skills: str = skills_api.get_latest_job_skills()
    return skills

@pytest.fixture(scope="session")
def indeed_scrapper(etl_configs: dict, job_skills: str) -> IndeedScrapper:
    """Fixture for Indeed scrapper"""
    return IndeedScrapper(etl_configs["data_sources"]["indeed"],job_skills)
