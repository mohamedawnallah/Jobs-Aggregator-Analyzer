import json
import pandas as pd
from loguru import logger
from typing import List
from app.pipeline.common.etls_common import ExtractorAsync
from pipeline.utilities.utils import Utils
import aiohttp
from pipeline.models.company_model import Company

class CompaniesInfoAPIExtractor(ExtractorAsync):
    def __init__(self, company_names_df: pd.DataFrame, companies_configs: dict, access_token: str):
        self.company_names_df = company_names_df
        self.access_token_headers = {"Authorization": f"Basic {access_token}"}
        self.companies_by_name_endpoint = companies_configs["by_name"]["url"]
        self.companies_by_name_method_type = companies_configs["by_name"]["method_type"]

    async def extract(self) -> List[dict]:
        """Get the Fortune 1000 Companies"""
        companies_data = []
        for _, row in self.company_names_df.iterrows():
            company_name = row["company_name"]
            company_data = await self.get_company_info(company_name)
            if company_data:
                companies_data.append(company_data)
        return companies_data
            
            
    async def get_company_info(self, company_name) -> dict:
        companies_by_name_endpoint = self.companies_by_name_endpoint % {"company_name": company_name}
        try:
            response = await Utils.request_url(url=companies_by_name_endpoint, http_method=self.companies_by_name_method_type, headers=self.access_token_headers)
            html = await response.text()
            companies_data: dict = json.loads(html)
            companies_data["company_name_job_platform"] = company_name
            return companies_data
        except aiohttp.http_exceptions.HttpBadRequest as http_bad_request:
            logger.error("Http Bad Request: ", http_bad_request.args[0])
            return None

        

    
