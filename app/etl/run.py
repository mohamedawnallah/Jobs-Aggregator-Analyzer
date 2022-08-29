"""Main Module of the application

Running ETL of the data from the multiple websites and storing it into a DWH
for further analytics and visualization.
"""
import asyncio
from typing import Union, Generator
import os
from etl.utilities.utils import Utils
from etls.apis.lightcast_job_skills_etl import LightCastJobSkillsETL
from etls.scrappers.indeed_etl import IndeedETL
from etl.models.lighcast_credentials_model import LightCastCredentials
from etl.extractors.apis.lightcast.job_skills_apis import LightCastJobSkillsAPIs
from etls.apis.fortune_1000_companies_etl import Fortune1000CompaniesETL
from etl.models.country_model import Country

async def main(params: dict):
    """Main entrypoint for ETLs across different scrappers"""
    etl_configs_input: dict = params["etl_configs"]
    countries: Union[Generator[Country,None,None],None] = params["countries"]
    job_title: str = params["job_title"]
    csv_file_path_input: str = params["csv_file_path"]
    pages_no: Union[int,None] = params["pages_no"]
    lightcast_credentials: LightCastCredentials = params["lightcast_credentials"]

    lightcast_job_skills_etl = LightCastJobSkillsETL(etl_configs_input, lightcast_credentials)
    job_skills: set[str] = await lightcast_job_skills_etl.run()

    # fortune_1000_companies_etl = Fortune1000CompaniesETL(etl_configs)
    # await fortune_1000_companies_etl.run()

    indeed_etl = IndeedETL(etl_configs,job_title,countries,
                           pages_no, job_skills, lightcast_cast_credentials, csv_file_path_input)
    await indeed_etl.run()


if __name__ == "__main__":
    PRODUCTION_ENV_FILE_PATH = "production.env"
    Utils.load_env_file(PRODUCTION_ENV_FILE_PATH)
    CONFIGS_PATH = "app/etl/settings/etl_configs.yaml"
    etl_configs: dict = Utils.get_configs(CONFIGS_PATH)

    LIGHTCAST_CLIENT_ID: str = os.getenv("LIGHTCAST_CLIENT_ID")
    LIGHTCAST_SECRET: str = os.getenv("LIGHTCAST_SECRET")
    LIGHTCAST_SCOPE: str = os.getenv("LIGHTCAST_SCOPE")
    LIGHTCAST_GRANT_TYPE: str = os.getenv("LIGHTCAST_GRANT_TYPE")
    lightcast_cast_credentials: LightCastCredentials = LightCastCredentials(LIGHTCAST_CLIENT_ID,LIGHTCAST_SECRET,LIGHTCAST_GRANT_TYPE,LIGHTCAST_SCOPE)

    JOB_TITLE = "data engineer"
    PAGES_NO = None
    CUSTOMIZED_COUNTRIES = None
    csv_file_path = f"app/etl/static/data/{JOB_TITLE}_jobs.csv"
    job_params = {"etl_configs":etl_configs,"countries":CUSTOMIZED_COUNTRIES,"job_title":JOB_TITLE,"pages_no": PAGES_NO,"csv_file_path":csv_file_path, "lightcast_credentials": lightcast_cast_credentials}

    asyncio.run(main(job_params))

