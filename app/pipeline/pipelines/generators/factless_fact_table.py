from typing import AsyncGenerator, Optional
import pandas as pd
from typing import List
import json
from common.etls_common import DataPipeline, Extractor, Transformer, Loader
from extractors.apis.companies.companies_info_api_extractor import CompaniesInfoAPIExtractor
from transformers.apis.companies.companies_info_api_transformer import CompaniesInfoAPITransformer
from app.utilities.decorators import timer
from pipeline.transformers.generators.factless_fact_table_transformer import FactlessFactTableTransformer

from loguru import logger

class FactlessFactTableETL(Transformer, Loader, DataPipeline):
    """Indeed ETL class"""
    def __init__(self, jobs_dim_df: pd.DataFrame, dates_dim_df: pd.DataFrame, locations_dim_df: pd.DataFrame, companies_dim_df: pd.DataFrame, staging_storage_path: str, production_storage_path: str):
        self.jobs_dim_df = jobs_dim_df
        self.dates_dim_df = dates_dim_df
        self.locations_dim_df = locations_dim_df
        self.companies_dim_df = companies_dim_df
        self.staging_storage_path = staging_storage_path
        self.production_storage_path = production_storage_path

    def transform(self) -> pd.DataFrame:
        """Transform data"""
        factless_fact_table_transformed: pd.DataFrame = FactlessFactTableTransformer.transform(self.jobs_dim_df, self.dates_dim_df, self.locations_dim_df, self.companies_dim_df)
        return factless_fact_table_transformed

    def load(self, companies_df: pd.DataFrame) -> bool:
        """Load data into the CSV"""
        companies_df.to_csv(self.production_storage_path)
        return True
    
    @timer
    async def run(self):
        """Run the ETL"""
        # companies_data: List[dict] = await self.extract()
        factless_fact_table_transformed_df: pd.DataFrame = self.transform()
        is_loaded: bool = self.load(factless_fact_table_transformed_df)
        return is_loaded
