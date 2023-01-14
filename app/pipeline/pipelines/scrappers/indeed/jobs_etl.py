from typing import List, Generator, Union, AsyncGenerator
import time
import json
import pandas as pd
from aiostream import stream
from extractors.scrappers.indeed.jobs_scrapper import IndeedJobsScrapper
from models.country_model import CountryDim
from common.etls_common import DataPipeline, Extractor, Transformer, Loader
from models.country_model import CountryDim
from models.job_model import JobDim
from pipeline.transformers.scrappers.indeed.jobs_transformer import IndeedJobsTransformer
from app.utilities.decorators import timer_async

class IndeedJobsETL(Extractor, Transformer, Loader, DataPipeline):
    """Indeed ETL class"""
    def __init__(self,indeed_etl_configs: dict,job_title: str,
                 countries: Generator[CountryDim,None,None],
                 pages_no: int, staging_csv_file_path: str, production_csv_file_path: str):
        self.indeed_etl_configs = indeed_etl_configs
        self.job_title = job_title
        self.countries = countries
        self.pages_no = pages_no
        self.file_name = "indeed_jobs.csv" 
        self.staging_csv_file_path = staging_csv_file_path % {"file_name": self.file_name}
        self.production_csv_file_path = production_csv_file_path % {"file_name": self.file_name}

    async def extract(self) -> pd.DataFrame:
        """Extract data from the Indeed Website"""
        indeed_scrapper = IndeedJobsScrapper(self.indeed_etl_configs)
        jobs_df = await indeed_scrapper.extract(self.countries, self.job_title, self.pages_no)
        jobs_df.to_csv(self.staging_csv_file_path, index=False)
        return jobs_df

    async def transform(self, jobs_df: pd.DataFrame) -> pd.DataFrame:
        """Transform data"""
        jobs_df = IndeedJobsTransformer.transform_df(jobs_df)
        return jobs_df

    def load(self, jobs_df: pd.DataFrame) -> bool:
        """Load data into the CSV"""
        jobs_df.to_csv(self.production_csv_file_path)
        return True

    @timer_async
    async def run(self):
        """Run the ETL"""
        jobs_df: pd.DataFrame = await self.extract()
        jobs_df_transformed =  await self.transform(jobs_df)
        is_loaded = self.load(jobs_df_transformed)
        return is_loaded




