import os
import json
import re
from typing import List
import requests
from dotenv import load_dotenv
from etl.utils.utils import Utils

class JobSkillsAPI:
    """Job Skills API"""
    def __init__(self, lightcast_skills_configs: dict):
        #Load Environment Variables
        load_dotenv("app/etl/.env")
        self.emsi_client_id: str = os.getenv("EMSI_CLIENT_ID")
        self.emsi_secret: str = os.getenv("EMSI_SECRET")
        self.emsi_scope: str = os.getenv("EMSI_SCOPE")
        self.lightcast_skills_configs: dict = lightcast_skills_configs
        self.lightcast_skills_endpoints: dict= self.lightcast_skills_configs["endpoints"]
        self.access_token = self.get_access_token()
        
    def get_access_token(self) -> str:
        """Get the access token"""
        auth_endpoint: str = self.lightcast_skills_endpoints["auth"]["url"]
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data: dict = {
            "grant_type": "client_credentials",
            "client_id": self.emsi_client_id,
            "client_secret": self.emsi_secret,
            "scope": self.emsi_scope
        }
        response: requests.Response = requests.post(auth_endpoint, headers=headers, data=data)
        access_token: str = response.json()["access_token"]
        return access_token

    def get_latest_job_skills(self) -> List[dict]:
        """Get the latest skills"""
        url = self.lightcast_skills_endpoints["latest_skills"]["url"]
        headers = {'Authorization': f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        all_job_skills: List[dict] = json.loads(response.text)["data"]
        job_skills: str = JobSkillsAPI._get_valid_job_skills(all_job_skills)
        return job_skills

    @staticmethod
    def _get_valid_job_skills(all_job_skills: List[dict]) -> str:
        """Get the valid job skills"""
        job_skills: str = ""
        for job_skill in all_job_skills:
            skill_name = job_skill["name"].lower().strip()
            short_skill_name_search_pattern: str = r"\(([a-zA-Z\s]+)\)"
            skill_matched: re.Match = re.search(short_skill_name_search_pattern, skill_name)
            if skill_matched:
                short_skill_name = skill_matched.groups()[0].strip()
                start_indx, last_indx = skill_matched.span()
                skill_name = skill_name.replace(skill_name[start_indx:last_indx],"").strip()
                skill_name += f" | {short_skill_name}"
            job_skills += skill_name + ", "
        return job_skills

    def get_skills_from_text(self, job_description: str) -> dict:
        """Get the skills from text"""
        url = self.lightcast_skills_endpoints["extract_skills_from_text"]["url"]
        querystring = {"language":"en"}
        payload = "{ \"text\": \"" + job_description + "\" }"
        headers = {
            'Authorization': f"Bearer {self.access_token}",
            'Content-Type': "application/json"
        }
        response = requests.request("POST", url, data=payload.encode("utf-8"), headers=headers, params=querystring)
        print(response.text)
        job_skills: dict = json.loads(response.text)
        return job_skills

if __name__ == "__main__":
    job_skills_api = JobSkillsAPI()
    result: str = job_skills_api.get_latest_skills()
    result = result.split(", ")
    print(result[:100])