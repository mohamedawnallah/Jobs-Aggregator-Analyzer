from typing import List
import pandas as pd
import json
from etl.extractors.apis.fortune_companies.fortune_1000_companies_api import Fortune1000CompaniesAPI
from common.etls_common import Extractor, Transformer, Loader, ETL
from transformers.apis.fortune_companies_transformer import Fortune1000CompaniesTransformer

class Fortune1000CompaniesETL(Extractor, Transformer, Loader, ETL):
    """Fortune 1000 Companies ETL"""
    def __init__(self, etl_configs: dict):
        self.etl_configs = etl_configs
    
    async def extract(self) -> pd.DataFrame:
        """Extract data from the Fortune 1000 Companies Website"""
        fortune_1000_companies_etl_staging_csv_file: str = "app/etl/static/staging/fortune_1000_companies_staging.json"
        fortune_1000_companies_api = Fortune1000CompaniesAPI(self.etl_configs)
        fortune_1000_companies: List[dict] = await fortune_1000_companies_api.get_fortune_1000_companies()
        with open(fortune_1000_companies_etl_staging_csv_file, "w",encoding="utf-8") as f:
            f.write(json.dumps(fortune_1000_companies,indent=4))
        return fortune_1000_companies

    def transform(self, fortune_1000_companies: List[dict]) -> pd.DataFrame:
        """Transform data"""
        fortune_1000_companies_meta_data: dict = fortune_1000_companies[0]
        fortune_1000_companies_data: dict = fortune_1000_companies[1]
        print(json.dumps(fortune_1000_companies_meta_data,indent=4))
        fortune_1000_companies_df: pd.DataFrame = Fortune1000CompaniesTransformer.transform(fortune_1000_companies_meta_data, fortune_1000_companies_data)
        return fortune_1000_companies_df

    def load(self, fortune_1000_companies_df: pd.DataFrame) -> None:
        """Load data to the database"""
        fortune_1000_companies_etl_csv_file: str = "app/etl/static/data/fortune_1000_companies.json"
        with open(fortune_1000_companies_etl_csv_file, "w",encoding="utf-8") as f:
            f.write(json.dumps(fortune_1000_companies_df.to_dict(orient="records"),indent=4))
        return fortune_1000_companies_df

    async def run(self) -> None:
        """Run the ETL"""
        fortune_1000_companies_df: pd.DataFrame = await self.extract()
        fortune_1000_companies_transformed_df: pd.DataFrame = self.transform(fortune_1000_companies_df)
        loaded: bool = self.load(fortune_1000_companies_transformed_df)
        print("Loaded: ", loaded)
