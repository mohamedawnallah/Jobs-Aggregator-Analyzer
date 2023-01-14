from typing import AsyncGenerator, Optional
import pandas as pd
from common.etls_common import DataPipeline, Extractor, Transformer, Loader
from extractors.scrappers.indeed.countries_scrapper import IndeedCountriesScrapper
from pipeline.models.country_model import CountryDim
from pipeline.utilities.utils import Utils
from pipeline.transformers.scrappers.indeed.countries_transformer import IndeedCountriesTransformer
from app.utilities.decorators import timer, timer_async
from loguru import logger

class IndeedCountriesETL(Extractor, Transformer, Loader, DataPipeline):
    """Indeed ETL class"""
    def __init__(self, countries_url: str, staging_csv_file_path: str, production_csv_file_path: str, countries_no: Optional[int] = None):
        self.countries_url = countries_url
        self.countries_no = countries_no
        self.file_name = "indeed_countries.csv"
        self.staging_csv_file_path = staging_csv_file_path % {"file_name": self.file_name}
        self.production_csv_file_path = production_csv_file_path % {"file_name": self.file_name}

    async def extract(self) -> pd.DataFrame:
        """Extract data from the Indeed Website"""
        indeed_countries_scrapper = IndeedCountriesScrapper()
        countries_df: pd.DataFrame = await indeed_countries_scrapper.extract(self.countries_url, self.countries_no)
        countries_df.to_csv(self.staging_csv_file_path, index=False)
        return countries_df

    def transform(self, countries_df: pd.DataFrame) -> pd.DataFrame:
        """Transform data"""
        transformed_df: pd.DataFrame = IndeedCountriesTransformer.transform_df(countries_df)
        return transformed_df

    def load(self, countries_df: pd.DataFrame) -> bool:
        """Load data into the CSV"""
        countries_df.to_csv(self.production_csv_file_path)
        return True
    
    @timer_async
    async def run(self):
        """Run the ETL"""
        countries_df: pd.DataFrame = await self.extract()
        jobs_transformed_df: pd.DataFrame = self.transform(countries_df)
        is_loaded: bool = self.load(jobs_transformed_df)
        return is_loaded
