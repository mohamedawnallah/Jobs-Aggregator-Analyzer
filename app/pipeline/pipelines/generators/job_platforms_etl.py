from typing import AsyncGenerator, Optional, Generator
import pandas as pd
from common.etls_common import DataPipeline, Extractor, Transformer, Loader
from extractors.generators.job_platforms_generator import JobPlatformsGenerator
from transformers.generators.job_platforms_transformer import JobPlatformsTransformer
from pipeline.models.country_model import CountryDim
from models.job_platform_model import JobPlatformDim
from utilities.decorators import timer
from loguru import logger

class JobPlatformsETL(Extractor, Transformer, Loader, DataPipeline):
    """Indeed ETL class"""
    def __init__(self, job_platforms_configs: dict[str, str], staging_csv_file_path: str, production_csv_file_path: str):
        self.job_platforms_configs = job_platforms_configs
        self.file_name = "job_platforms.csv"
        self.staging_csv_file_path = staging_csv_file_path % {"file_name": self.file_name}
        self.production_csv_file_path = production_csv_file_path % {"file_name": self.file_name}

    def extract(self) -> pd.DataFrame:
        """Extract data from the Indeed Website"""
        job_platforms_generator = JobPlatformsGenerator()
        job_platforms_gener: Generator[JobPlatformDim, None, None] = job_platforms_generator.get_job_platforms(self.job_platforms_configs)
        countries_df: pd.DataFrame =  job_platforms_generator.get_job_platforms_df(job_platforms_gener)
        countries_df.to_csv(self.staging_csv_file_path)
        return countries_df

    def transform(self, job_platforms_df: pd.DataFrame) -> pd.DataFrame:
        """Transform data"""
        job_platforms_transformed_df: pd.DataFrame = JobPlatformsTransformer.transform_df(job_platforms_df)
        return job_platforms_transformed_df

    def load(self, job_platforms_df: pd.DataFrame) -> bool:
        """Load data into the CSV"""
        job_platforms_df.to_csv(self.production_csv_file_path)
        return True
    
    @timer
    def run(self):
        """Run the ETL"""
        job_platforms_df: pd.DataFrame = self.extract()
        job_platforms_transformed_df: pd.DataFrame = self.transform(job_platforms_df)
        is_loaded: bool = self.load(job_platforms_transformed_df)
        return is_loaded
