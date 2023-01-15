from typing import AsyncGenerator, Optional
import pandas as pd
import json
from common.etls_common import DataPipeline, Extractor, Transformer, Loader
from extractors.scrappers.indeed.countries_scrapper import IndeedCountriesScrapper
from pipeline.models.country_model import CountryDim
from pipeline.utilities.utils import Utils
from app.utilities.decorators import timer
from transformers.connections.fortune_companies_info_transformer import FortuneCompaniesInfoTransformer
from loguru import logger

class FortuneCompaniesInfoETL(Transformer, Loader, DataPipeline):
    """Indeed ETL class"""
    def __init__(self, companies_df: pd.DataFrame, fortune_companies_df: pd.DataFrame, gold_storage_path: str):
        self.companies_df = companies_df
        self.fortune_companies_df = fortune_companies_df
        self.gold_storage_path = gold_storage_path
        
    def transform(self) -> pd.DataFrame:
        """Transform data"""
        fortune_companies_info_merged_df: pd.DataFrame = FortuneCompaniesInfoTransformer.transform(self.companies_df, self.fortune_companies_df)
        return fortune_companies_info_merged_df

    def load(self, fortune_companies_info_merged_df: pd.DataFrame) -> bool:
        """Load data into the CSV"""
        fortune_companies_info_merged_df.to_csv(self.gold_storage_path)
        return True
    
    @timer
    def run(self):
        """Run the ETL"""
        fortune_companies_info_merged_df: pd.DataFrame = self.transform()
        is_loaded: bool = self.load(fortune_companies_info_merged_df)
        return is_loaded
