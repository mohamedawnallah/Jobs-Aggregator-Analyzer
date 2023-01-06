import json
import pandas as pd
from typing import List
from app.pipeline.common.etls_common import ExtractorAsync
from pipeline.utilities.utils import Utils

class CompaniesInfoAPIExtractor(ExtractorAsync):
    def __init__(self, company_names_df: pd.DataFrame, companies_configs: dict, access_token: str):
        self.company_names_df = company_names_df
        self.access_token = access_token
        self.companies_by_name_endpoint = companies_configs["by_name"]["url"]
        self.companies_by_name_method_type = companies_configs["by_name"]["method_type"]
    
    async def extract(self) -> pd.DataFrame:
        """Get the Fortune 1000 Companies"""
        companies_df: pd.DataFrame = await self.get_companies_info()
        return companies_df
            
    async def get_companies_info(self) -> pd.DataFrame:
        response: str = await Utils.request_url(url=self.companies_by_name_endpoint, http_method=self.companies_by_name_method_type)
        companies_df: dict = json.loads(response)
        return fortune_companies_df
    
