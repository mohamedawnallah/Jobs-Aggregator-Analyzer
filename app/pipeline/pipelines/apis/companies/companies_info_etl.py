from typing import AsyncGenerator, Optional
import pandas as pd
import json
from common.etls_common import DataPipeline, Extractor, Transformer, Loader
from extractors.apis.companies.companies_info_api_extractor import CompaniesInfoAPIExtractor
from pipeline.transformers.scrappers.indeed.countries_transformer import IndeedCountriesTransformer
from utilities.decorators import timer, timer_async
from pipeline.transformers.apis.fortune_companies_transformer import FortuneCompaniesAPITransformer
from loguru import logger

class CompaniesETL(Extractor, Transformer, Loader, DataPipeline):
    """Indeed ETL class"""
    def __init__(self, company_names_df: pd.DataFrame, companies_configs: dict, access_token: str, staging_storage_path: str, production_storage_path: str):
        self.company_names_df = company_names_df
        self.companies_configs = companies_configs
        self.access_token = access_token
        self.staging_storage_path = staging_storage_path
        self.production_storage_path = production_storage_path

    async def extract(self) -> pd.DataFrame:
        """Extract data from the Indeed Website"""
        companies_api_extractor = CompaniesInfoAPIExtractor(self.company_names_df, self.companies_configs, self.access_token)
        companies_df: pd.DataFrame = await companies_api_extractor.extract()
        return companies_df

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
