import aiohttp
import json
from typing import List


class Fortune1000CompaniesAPI:
    def __init__(self, etl_configs: dict):
        self.fortune_1000_companies_configs = etl_configs["data_sources"]["fortune_1000_companies"]
    
    async def get_fortune_1000_companies(self) -> List[dict]:
        """Get the Fortune 1000 Companies"""
        latest_fortune_1000_companies_url: str = self.fortune_1000_companies_configs["url"]
        method_type: str = self.fortune_1000_companies_configs["method_type"]
        async with aiohttp.ClientSession() as session:
            fortune_1000_companies_response = await session.request(method=method_type,url=latest_fortune_1000_companies_url)
            fortune_1000_companies_response_json: str = await fortune_1000_companies_response.text()
            fortune_1000_companies_with_meta_data: List[dict] = json.loads(fortune_1000_companies_response_json)
        return fortune_1000_companies_with_meta_data
                    