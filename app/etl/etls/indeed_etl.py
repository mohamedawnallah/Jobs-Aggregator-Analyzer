from typing import Iterator, Optional
from etl.scrappers.indeed_scrapper import IndeedScrapper
from etl.models.job_dataclasses import JobFullInfo
from etl.loaders.indeed_loaders import IndeedPersistenceManager
from etl.utils.job_specifications import BaseSpecification
from etl.utils.etls_common import Extractor, Loader
from etl.models.job_dataclasses import Country
from etl.utils.utils import Utils
class IndeedETL(Extractor, Loader):
    """Indeed ETL class"""
    def __init__(self,configs: dict, job_title: str, job_skills: BaseSpecification):
        self.configs = configs
        self.job_title = job_title
        self.job_skills = job_skills

    def extract(self, customized_countries: Iterator[Country] = None, countries_no: int=None, jobs_pages_no: Optional[int] = None) -> Iterator[dict]:
        """Extract data from the Indeed Website"""
        indeed_scrapper = IndeedScrapper(self.configs, self.job_skills)
        if not customized_countries:
            countries = indeed_scrapper.get_countries(countries_no)
        if customized_countries:
            countries = customized_countries
        jobs_countries: Iterator[Iterator[Iterator[JobFullInfo]]] = indeed_scrapper.get_jobs_countries(countries, self.job_title, jobs_pages_no)
        jobs_countries: Iterator[JobFullInfo] = IndeedScrapper.get_indeed_job_item_generator(jobs_countries)
        return jobs_countries

    def load(self,csv_file_path: str,jobs_countries: Iterator[Iterator[JobFullInfo]]) -> int:
        """Load data into the CSV"""
        result = IndeedPersistenceManager.write_to_csv(csv_file_path, jobs_countries)
        return result

