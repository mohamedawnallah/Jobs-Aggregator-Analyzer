from typing import AsyncGenerator, Optional
import pandas as pd
import json
from common.etls_common import DataPipeline, Extractor, Transformer, Loader
from extractors.scrappers.indeed.countries_scrapper import IndeedCountriesScrapper
from pipeline.models.country_model import CountryDim
from pipeline.utilities.utils import Utils
from app.utilities.decorators import timer_async
from loguru import logger

class FortuneCompaniesInfoETL(Extractor, Transformer, Loader, DataPipeline):
    """Indeed ETL class"""
    def __init__(self, fortune_companies_configs: dict, staging_storage_path: str, raw_storage_path: str):
        self.fortune_companies_configs = fortune_companies_configs
        self.raw_storage_path = raw_storage_path
        self.staging_storage_path = staging_storage_path

    async def extract(self) -> pd.DataFrame:
        """Extract data from the Indeed Website"""
        fortune_companies_api_extractor = FortuneCompaniesAPIExtractor(self.fortune_companies_configs)
        fortune_companies: dict = await fortune_companies_api_extractor.extract()
        with open(self.raw_storage_path, "w",encoding='utf-8') as file_handler:
            file_handler.write(json.dumps(fortune_companies))
        return fortune_companies

    def transform(self, fortune_companies: dict) -> pd.DataFrame:
        """Transform data"""
        fortune_companies_df: pd.DataFrame = FortuneCompaniesAPITransformer.transform(fortune_companies)
        fortune_companies_transformed_df: pd.DataFrame = FortuneCompaniesAPITransformer.transform_df(fortune_companies_df)
        return fortune_companies_transformed_df

    def load(self, fortune_companies_df: pd.DataFrame) -> bool:
        """Load data into the CSV"""
        fortune_companies_df.to_csv(self.staging_storage_path)
        return True
    
    @timer_async
    async def run(self):
        """Run the ETL"""
        fortune_companies: dict = await self.extract()
        fortune_companies_transformed_df: pd.DataFrame = self.transform(fortune_companies)
        is_loaded: bool = self.load(fortune_companies_transformed_df)
        return is_loaded
