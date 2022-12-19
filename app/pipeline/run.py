"""Main Module of the application

Running ETL of the data from the multiple websites and storing it into a DWH
for further analytics and visualization.
"""
import asyncio
import pandas as pd
from typing import Union, Generator
import os
from pipeline.utilities.utils import Utils
#from etl.utilities.utils import Utils
#from etls.apis.lightcast_job_skills_etl import LightCastJobSkillsETL
#from etls.scrappers.indeed.indeed_etl import IndeedETL
from pipeline.models.lighcast_credentials_model import LightCastCredentials
#from etl.extractors.apis.lightcast.job_skills_apis import LightCastJobSkillsAPIs
#from etls.apis.fortune_1000_companies_etl import Fortune1000CompaniesETL
from pipelines.scrappers.indeed.countries_etl import IndeedCountriesETL
from pipeline.extractors.scrappers.indeed.countries_scrapper import IndeedCountriesScrapper
from pipelines.scrappers.indeed.jobs_etl import IndeedJobsETL
from pipelines.generators.job_platforms_etl import JobPlatformsETL
from pipelines.generators.date_dimensions_etl import DateDimensionsETL
from pipelines.scrappers.language_translation.language_translation_etl import LanguageTranslationETL
from pipelines.apis.fortune_companies_etl import FortuneCompaniesETL

from models.country_model import CountryDim

async def main(params: dict):
    """Main entrypoint for ETLs across different scrappers"""
    pipeline_configs: dict = params["pipeline_configs"]
    start_date, end_date = params["start_date"], params["end_date"]
    job_title = params["job_title"]
    pages_no = params["pages_no"]
    
    data_sources_configs: dict = pipeline_configs["data_sources"]
    job_platforms_configs: dict = data_sources_configs["job_platforms"]
    company_platforms_configs: dict = data_sources_configs["company_platforms"]
    fortune_companies_configs = company_platforms_configs["fortune_companies"]
    helpers_data_sources_configs: dict = data_sources_configs["helpers"]
    storage_configs: dict = pipeline_configs["storage"]
    
    indeed_configs: dict = job_platforms_configs["indeed"]
    staging_storage_path = storage_configs["staging"]["csv"]
    production_storage_path = storage_configs["production"]["csv"]
    indeed_countries_url = indeed_configs["countries_url"]
    
    # countries: Union[Generator[Country,None,None],None] = params["countries"]
    # job_title: str = params["job_title"]
    # csv_file_path_input: str = params["csv_file_path"]
    # pages_no: Union[int,None] = params["pages_no"]
    # lightcast_credentials: LightCastCredentials = params["lightcast_credentials"]

    # lightcast_job_skills_etl = LightCastJobSkillsETL(etl_configs_input, lightcast_credentials)
    # job_skills: set[str] = await lightcast_job_skills_etl.run()

    staging_file_name, production_file_name = "fortune_companies.json", "fortune_companies.csv"
    staging_path_fortune_companies = staging_storage_path % {"file_name":staging_file_name}
    production_path_fortune_companies = production_storage_path % {"file_name":production_file_name}
    fortune_1000_companies_etl = FortuneCompaniesETL(fortune_companies_configs, staging_path_fortune_companies, production_path_fortune_companies)
    await fortune_1000_companies_etl.run()

    
    # indeed_countries_etl = IndeedCountriesETL(indeed_countries_url, staging_storage_path, production_storage_path)
    # await indeed_countries_etl.run()
    
    # job_platforms_etl = JobPlatformsETL(job_platforms_configs, staging_storage_path, production_storage_path)
    # job_platforms_etl.run()
    
    # date_dimensions_etl = DateDimensionsETL(start_date, end_date, staging_storage_path, production_storage_path)
    # date_dimensions_etl.run()
    
    # countries_production_path = production_storage_path % {"file_name":"indeed_countries.csv"}
    # countries = IndeedCountriesScrapper.get_countries_from_local(countries_production_path)
    # jobs_etl = IndeedJobsETL(indeed_configs, job_title, countries, pages_no, staging_storage_path, production_storage_path)
    # await jobs_etl.run()
    
    # jobs_production_path = production_storage_path % {"file_name":"indeed_jobs.csv"}
    # jobs_df = pd.read_csv(jobs_production_path)
    # columns_to_translate = ["job_title","job_description","job_benefits","job_city"]
    # google_translation_etl = LanguageTranslationETL(jobs_df, columns_to_translate, jobs_production_path)
    # await google_translation_etl.run()
    
    

    
    

if __name__ == "__main__":
    CONFIGS_PATH = "app/pipeline/settings/pipeline_configs.yaml"
    pipeline_configs: dict = Utils.get_configs(CONFIGS_PATH)

    LIGHTCAST_CLIENT_ID: str = os.getenv("LIGHTCAST_CLIENT_ID")
    LIGHTCAST_SECRET: str = os.getenv("LIGHTCAST_SECRET")
    LIGHTCAST_SCOPE: str = os.getenv("LIGHTCAST_SCOPE")
    LIGHTCAST_GRANT_TYPE: str = os.getenv("LIGHTCAST_GRANT_TYPE")
    lightcast_cast_credentials: LightCastCredentials = LightCastCredentials(LIGHTCAST_CLIENT_ID,LIGHTCAST_SECRET,LIGHTCAST_GRANT_TYPE,LIGHTCAST_SCOPE)

    job_title, countries, pages_no = "data+engineer", None, 2
    start_date = "2021-01-01"
    end_date = "2050-12-31"
    job_params = {"pipeline_configs":pipeline_configs,"countries":countries,
                  "job_title":job_title,"pages_no": pages_no,
                  "lightcast_credentials": lightcast_cast_credentials,
                  "start_date": start_date, "end_date": end_date}
    
    asyncio.run(main(job_params))

