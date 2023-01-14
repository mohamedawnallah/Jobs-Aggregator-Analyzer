import json
import pandas as pd
from typing import List
from app.pipeline.common.etls_common import ExtractorAsync
from pipeline.utilities.utils import Utils

class FortuneCompaniesAPIExtractor(ExtractorAsync):
    def __init__(self, fortune_companies_configs: dict):
        self.fortune_companies_url = fortune_companies_configs["url"]
        self.fortune_companies_method_type = fortune_companies_configs["method_type"]
    
    async def extract(self) -> List[dict]:
        """Get the Fortune 1000 Companies"""
        fortune_companies_df: dict = await self.get_fortune_companies()
        return fortune_companies_df
            
    async def get_fortune_companies(self) -> List[dict]:
        response: str = await Utils.request_url(url=self.fortune_companies_url, http_method=self.fortune_companies_method_type)
        fortune_companies_df: dict = json.loads(response)
        return fortune_companies_df
    
