from typing import List, Generator, Union
import time
import json
import pandas as pd
from aiostream import stream
from etl.extractors.scrappers.indeed_scrapper import IndeedScrapper
from models.job_models import JobCountry
from common.etls_common import ETL, Extractor, Transformer, Loader
from etl.models.country_model import Country
from transformers.scrappers.indeed_transformer import IndeedJobSkillsTransformer
from etl.models.lighcast_credentials_model import LightCastCredentials
from etl.utilities.utils import Utils
from pandarallel import pandarallel

class IndeedETL(Extractor, Transformer, Loader, ETL):
    """Indeed ETL class"""
    def __init__(self,etl_configs: dict,job_title: str,
                 countries: Generator[Country,None,None],
                 pages_no: int,job_skills: str, lightcast_credentials: LightCastCredentials,
                csv_file_path: str):
        self.etl_configs = etl_configs
        self.job_title = job_title
        self.countries = countries
        self.pages_no = pages_no
        self.job_skills = job_skills
        self.lightcast_credentials = lightcast_credentials
        self.csv_file_path = csv_file_path

    async def extract(self) -> pd.DataFrame:
        """Extract data from the Indeed Website"""
        staging_csv_file: str = f"app/etl/static/staging/{self.job_title}_staging.csv"
        indeed_scrapper = IndeedScrapper(self.etl_configs)
        if not self.countries:
            self.countries =  indeed_scrapper.get_countries()
        jobs_countries: Generator[JobCountry,None,None] = indeed_scrapper.get_jobs_countries(self.countries, self.job_title)
        indeed_job_items_generators: List[Generator[dict,None,None]] = [IndeedScrapper.get_indeed_job_items(job_country,indeed_scrapper, self.pages_no) async for job_country in jobs_countries]
        jobs_staging_df: pd.DataFrame = await IndeedETL._get_jobs_streams_df(indeed_job_items_generators)
        jobs_staging_df: pd.DataFrame = jobs_staging_df.to_csv(staging_csv_file)
        return jobs_staging_df

    @staticmethod
    async def _get_jobs_streams_df(indeed_job_items_generators: List[Generator[dict,None,None]]) -> pd.DataFrame:
        """Saving Streams to staging csv"""
        jobs_df: Union[pd.DataFrame, None] = None
        combined_indeed_jobs_steams = stream.merge(*indeed_job_items_generators)
        indx = 0
        async with combined_indeed_jobs_steams.stream() as streamer:
            async for item in streamer:
                if indx == 0:
                    jobs_df = pd.DataFrame(item,index=[indx])
                else:
                    jobs_df = pd.concat([jobs_df,pd.DataFrame(item,index=[indx])],axis=0)
                indx += 1
                print(json.dumps(item,indent=4))
        return jobs_df

    async def transform(self, jobs_df: pd.DataFrame) -> pd.DataFrame:
        """Transform data"""
        pandarallel.initialize(progress_bar=True)
        start = time.perf_counter()
                  
        jobs_df["job_skills"] = jobs_df["job_description"].parallel_apply(lambda job_description:  IndeedJobSkillsTransformer.get_job_skills(self.job_skills,job_description))
        # jobs_df["job_skills"] = jobs_df["job_skills"].apply(IndeedJobSkillsTransformer.transform)
        elapsed = time.perf_counter() - start
        print(f"Time Elapsed is: {elapsed: 0.4f} seconds")
        return jobs_df

    def load(self, jobs_df: pd.DataFrame) -> bool:
        """Load data into the CSV"""
        jobs_df.to_csv(self.csv_file_path)
        return 1

    async def run(self):
        """Run the ETL"""
        # jobs_df: pd.DataFrame = await self.extract()
        jobs_df: pd.DataFrame = pd.read_csv("app/etl/static/data/data engineer_jobs.csv")
        jobs_transformed_df: pd.DataFrame = await self.transform(jobs_df)
        return None
        result: bool = self.load(jobs_transformed_df)
        print(jobs_transformed_df['job_skills'])
        return result

