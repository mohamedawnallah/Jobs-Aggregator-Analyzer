import json
from typing import List
import aiohttp
from etl.extractors.apis.lightcast.access_token_api import LightCastAccessTokenGenerator
from etl.models.lighcast_credentials_model import LightCastCredentials

class LightCastJobSkillsAPIs:
    """Job Skills API"""
    def __init__(self, etl_configs: str, lightcast_credentials: LightCastCredentials):
        self.lightcast_configs: dict = etl_configs["data_sources"]["lightcast"]
        self.access_token_api: dict = self.lightcast_configs["auth"]
        self.lightcast_credentials: LightCastCredentials = lightcast_credentials
        self.lightcast_client_id: str = self.lightcast_credentials.lightcast_client_id
        self.lightcast_grant_type: str = self.lightcast_credentials.lightcast_grant_type
        self.lightcast_scope: str = self.lightcast_credentials.lightcast_scope
        self.lightcast_secret: str = self.lightcast_credentials.lightcast_secret
        self.job_skills_api: dict = self.lightcast_configs["lightcast_skills"]["endpoints"]["latest_skills"]
        self.access_token: str = ""

    async def get_latest_job_skills(self) -> List[dict]:
        """Get the latest skills"""
        self.access_token = await LightCastAccessTokenGenerator.get_access_token(self.access_token_api, self.lightcast_grant_type, self.lightcast_client_id, self.lightcast_secret, self.lightcast_scope)
        latest_skills_url: str = self.job_skills_api["url"]
        method_type: str = self.job_skills_api["method_type"]
        while True:
            headers = {'Authorization': f"Bearer {self.access_token}"}
            async with aiohttp.ClientSession(headers=headers) as session:
                response = await session.request(method=method_type,url=latest_skills_url,headers=headers)
                response_text = await response.text()
            if response.status == 401:
                self.access_token = await LightCastAccessTokenGenerator.get_access_token(self.access_token_api, self.lightcast_credentials, self.lightcast_client_id, self.lightcast_secret, self.lightcast_scope)
                continue
            break
        try:
            all_job_skills: List[dict] = json.loads(response_text)["data"]
        except KeyError as key_error:
            print(key_error)
            return None
        return all_job_skills

