from typing import List
import pandas as pd
from extractors.apis.fortune_companies.fortune_companies_api_extractor import Fortune1000CompaniesAPI
from common.etls_common import Extractor, Transformer, Loader, ETL
from extractors.apis.lightcast.job_skills_apis import LightCastJobSkillsAPIs
from models.lighcast_credentials_model import LightCastCredentials
from transformers.apis.lightcast_transformer import LightCastJobSkillsTransformer

class LightCastJobSkillsETL(Extractor, Transformer, Loader, ETL):
    """Fortune 1000 Companies ETL"""
    def __init__(self, etl_configs: dict, lightcast_credentials: LightCastCredentials):
        self.etl_configs = etl_configs
        self.lightcast_credentials = lightcast_credentials
    
    async def extract(self) -> List[dict]:
        """Extract data from the Fortune 1000 Companies Website"""
        lightcast_job_skills_api = LightCastJobSkillsAPIs(self.etl_configs, self.lightcast_credentials)
        latest_job_skills: List[dict] = await lightcast_job_skills_api.get_latest_job_skills()
        return latest_job_skills

    def transform(self, latest_job_skills: List[dict]) -> set[str]:
        """Transform data"""
        job_skills_transformed: set[str] = LightCastJobSkillsTransformer.transform(latest_job_skills)
        return job_skills_transformed

    def load(self, job_skills_transformed: set[str]) -> set[str]:
        """Load data"""
        return job_skills_transformed

    async def run(self) -> None:
        """Run the ETL"""
        latest_job_skills: List[dict] = await self.extract()
        job_skills_transformed: set[str] = self.transform(latest_job_skills)
        job_skills: set[str] = self.load(job_skills_transformed)
        return job_skills
