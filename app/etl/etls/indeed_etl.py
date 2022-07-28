from typing import Iterator, Optional
import pandas as pd
from etl.scrappers.indeed_scrapper import IndeedScrapper
from models.job_models import JobFullInfo
from etl.loaders.indeed_loaders import IndeedPersistenceManager
from etl.utils.job_specifications import BaseSpecification
from etl.utils.etls_common import ETL, Extractor, Transformer, Loader
from models.job_models import Country
from etl.utils.utils import Utils
class IndeedETL(Extractor, Transformer, Loader, ETL):
    """Indeed ETL class"""
    def __init__(self,configs: dict,job_title: str,
                 countries: Iterator[Country],
                 pages_no: int,job_skills: str, csv_file_path: str):
        self.configs = configs
        self.job_title = job_title
        self.countries = countries
        self.pages_no = pages_no
        self.job_skills = job_skills
        self.csv_file_path = csv_file_path

    def extract(self) -> pd.DataFrame:
        """Extract data from the Indeed Website"""
        indeed_scrapper = IndeedScrapper(self.configs,self.job_skills)
        jobs_countries: Iterator[Iterator[Iterator[JobFullInfo]]] = indeed_scrapper.get_jobs_countries(self.countries, self.job_title, self.pages_no)
        jobs_countries: Iterator[dict] = IndeedScrapper.get_indeed_job_items_generator(jobs_countries)
        jobs_df: pd.DataFrame = pd.DataFrame(jobs_countries)
        return jobs_df
    
    def transform(self, jobs_df: pd.DataFrame) -> pd.DataFrame:
        """Transform data"""
        pass

    def load(self, jobs_df: pd.DataFrame) -> bool:
        """Load data into the CSV"""
        jobs_df.to_csv(self.csv_file_path)
        return 1

    def run(self):
        """Run the ETL"""
        jobs_df: pd.DataFrame = self.extract()
        # jobs_transformed_df: pd.DataFrame = self.transform(jobs_df)
        result: bool = self.load(jobs_df)
        print(result)
        return result

