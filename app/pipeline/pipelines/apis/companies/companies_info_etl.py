from typing import AsyncGenerator, Optional
import pandas as pd
from typing import List
import json
from common.etls_common import DataPipeline, Extractor, Transformer, Loader
from extractors.apis.companies.companies_info_api_extractor import CompaniesInfoAPIExtractor
from transformers.apis.companies.companies_info_api_transformer import CompaniesInfoAPITransformer
from app.utilities.decorators import timer, timer_async
# from pipeline.transformers.apis.companies_info_api_transformer import CompaniesInfoAPITransformer
from loguru import logger

class CompaniesETL(Extractor, Transformer, Loader, DataPipeline):
    """Indeed ETL class"""
    def __init__(self, company_names_df: pd.DataFrame, companies_configs: dict, access_token: str, staging_storage_path: str, production_storage_path: str):
        self.company_names_df = company_names_df
        self.companies_configs = companies_configs
        self.access_token = access_token
        self.staging_storage_path = staging_storage_path
        self.production_storage_path = production_storage_path

    async def extract(self) -> List[dict]:
        """Extract data from the Indeed Website"""
        companies_api_extractor = CompaniesInfoAPIExtractor(self.company_names_df, self.companies_configs, self.access_token)
        companies_data: dict = await companies_api_extractor.extract()
        with open(self.staging_storage_path, "w",encoding='utf-8') as file_handler:
            file_handler.write(json.dumps(companies_data, indent=4))
        return companies_data

    def transform(self, companies_data: List[dict]) -> pd.DataFrame:
        """Transform data"""
        companies_info_transformed_df: pd.DataFrame = CompaniesInfoAPITransformer.transform(companies_data)
        return companies_info_transformed_df

    def load(self, companies_df: pd.DataFrame) -> bool:
        """Load data into the CSV"""
        companies_df.to_csv(self.production_storage_path)
        return True
    
    @timer_async
    async def run(self):
        """Run the ETL"""
        # companies_data: List[dict] = await self.extract()
        with open(self.staging_storage_path, "r") as file:
            companies_data: List[dict] = json.load(file)
        companies_transformed_df: pd.DataFrame = self.transform(companies_data)
        is_loaded: bool = self.load(companies_transformed_df)
        return is_loaded
