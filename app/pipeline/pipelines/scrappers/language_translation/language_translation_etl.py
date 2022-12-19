from typing import List, Optional
import pandas as pd
from common.etls_common import DataPipeline, Transformer, Loader
from transformers.scrappers.language_translation.language_translation_transformer import LanguageTranslationTransformer
from pipeline.transformers.scrappers.indeed.countries_transformer import IndeedCountriesTransformer
from utilities.decorators import timer, timer_async
from deep_translator import GoogleTranslator

from loguru import logger

class LanguageTranslationETL(Transformer, Loader, DataPipeline):
    """Indeed ETL class"""
    def __init__(self, jobs_df: pd.DataFrame, columns_to_translate: List[str], production_csv_file_path: str):
        self.jobs_df = jobs_df
        self.columns_to_translate = columns_to_translate
        self.file_name = "indeed_jobs_translated.csv"
        self.production_csv_file_path = production_csv_file_path % {"file_name": self.file_name}

    async def transform(self) -> pd.DataFrame:
        """Transform data"""
        jobs_translated_df = await LanguageTranslationTransformer.transform_df(self.jobs_df, self.columns_to_translate)
        return jobs_translated_df

    def load(self, countries_df: pd.DataFrame) -> bool:
        """Load data into the CSV"""
        countries_df.to_csv(self.production_csv_file_path, index=False)
        return True
    
    @timer_async
    async def run(self):
        """Run the ETL"""
        jobs_translated_df_transformed: pd.DataFrame = await self.transform()
        is_loaded: bool = self.load(jobs_translated_df_transformed)
        return is_loaded
