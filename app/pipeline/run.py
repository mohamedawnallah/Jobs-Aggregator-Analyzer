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
from models.lighcast_credentials_model import LightCastCredentials
#from etl.extractors.apis.lightcast.job_skills_apis import LightCastJobSkillsAPIs
#from etls.apis.fortune_1000_companies_etl import Fortune1000CompaniesETL
from pipelines.scrappers.indeed.countries_etl import IndeedCountriesETL
from extractors.scrappers.indeed.countries_scrapper import IndeedCountriesScrapper
from pipelines.scrappers.indeed.jobs_etl import IndeedJobsETL
from pipelines.generators.job_platforms_etl import JobPlatformsETL
from pipelines.generators.date_dimensions_etl import DateDimensionsETL
from pipelines.generators.factless_fact_table import FactlessFactTableETL
# from pipelines.scrappers.language_translation.language_translation_etl import LanguageTranslationETL
# from pipelines.apis.fortune_companies.fortune_companies_etl import FortuneCompaniesETL
from pipelines.connections.fortune_companies_info_etl import FortuneCompaniesInfoETL
from pipelines.apis.companies.companies_info_etl import CompaniesETL

from models.country_model import CountryDim

async def main(params: dict):
    """Main entrypoint for ETLs across different scrappers"""
    pipeline_configs: dict = params["pipeline_configs"]
    start_date, end_date = params["start_date"], params["end_date"]
    job_title = params["job_title"]
    pages_no = params["pages_no"]
    
    lightcast_credentials: LightCastCredentials = params["lightcast_credentials"]
    companies_api_token: str = params["companies_api_token"]

    job_platforms_configs: dict = pipeline_configs["data_sources"]["job_platforms"]
    company_platforms_configs: dict = pipeline_configs["data_sources"]["company_platforms"]
    helpers_data_sources_configs: dict = pipeline_configs["data_sources"]["helpers"]
    
    indeed_configs: dict = job_platforms_configs["indeed"]
    indeed_countries_url = indeed_configs["countries_url"]
    
    fortune_companies_configs = company_platforms_configs["fortune_companies"]
    
    
    storage_configs: dict = pipeline_configs["storage"]
    bronze_storage_path = storage_configs["raw"]["csv"]
    silver_storage_path = storage_configs["staging"]["csv"]
    gold_storage_path = storage_configs["production"]["csv"]
    
    # countries: Union[Generator[Country,None,None],None] = params["countries"]
    # job_title: str = params["job_title"]
    # csv_file_path_input: str = params["csv_file_path"]
    # pages_no: Union[int,None] = params["pages_no"]
    # lightcast_credentials: LightCastCredentials = params["lightcast_credentials"]

    # lightcast_job_skills_etl = LightCastJobSkillsETL(etl_configs_input, lightcast_credentials)
    # job_skills: set[str] = await lightcast_job_skills_etl.run()

    # raw_file_name, staging_file_name = "fortune_companies.json", "fortune_companies.csv"
    # raw_path_fortune_companies = raw_storage_path % {"file_name":raw_file_name}
    # staging_path_fortune_companies = raw_storage_path % {"file_name":staging_file_name}
    # fortune_1000_companies_etl = FortuneCompaniesETL(fortune_companies_configs, raw_path_fortune_companies, staging_path_fortune_companies)
    # await fortune_1000_companies_etl.run()

    
    # indeed_countries_etl = IndeedCountriesETL(indeed_countries_url, raw_storage_path, raw_storage_path)
    # await indeed_countries_etl.run()
    
    # job_platforms_etl = JobPlatformsETL(job_platforms_configs, raw_storage_path, raw_storage_path)
    # job_platforms_etl.run()
    
    # date_dimensions_etl = DateDimensionsETL(start_date, end_date, raw_storage_path, raw_storage_path)
    # date_dimensions_etl.run()
    
    # bronze_countries_path = bronze_storage_path % {"file_name":"indeed_countries.csv"}
    # countries = IndeedCountriesScrapper.get_countries_from_local(bronze_countries_path)

    # bronze_jobs_path = bronze_storage_path % {"file_name":"jobs.csv"}
    # silver_jobs_path = silver_storage_path % {"file_name":"jobs.csv"}
    # gold_jobs_path = gold_storage_path % {"file_name":"jobs.csv"}
    # jobs_etl = IndeedJobsETL(indeed_configs, job_title, countries, pages_no, bronze_jobs_path, silver_jobs_path, gold_jobs_path)
    # await jobs_etl.run()
    
    # jobs_staging_path= staging_storage_path % {"file_name":"jobs.csv"}
    # jobs_translated_staging_path = staging_storage_path % {"file_name":"jobs_translated.csv"}
    # jobs_df = pd.read_csv(jobs_staging_path)
    # columns_to_translate = ["job_title","job_description","job_benefits","job_city"]
    # language_translation_etl = LanguageTranslationETL(jobs_df, columns_to_translate, jobs_translated_staging_path)
    # await language_translation_etl.run()
    
    # companies_api_configs = company_platforms_configs["the_companies_api"]["endpoints"]
    # companies_staging_path = staging_storage_path % {"file_name":"companies_info.json"}
    # companies_production_path = production_storage_path % {"file_name":"companies_info.csv"}
    # companies_path = "app/pipeline/static/data/staging/companies.csv"
    # company_names_df = pd.read_csv(companies_path)
    # comanies_etl = CompaniesETL(company_names_df, companies_api_configs, companies_api_token, companies_staging_path, companies_production_path)
    # await comanies_etl.run()
    
    # gold_storage_path = production_storage_path % {"file_name":"fortune_companies_info_merged.csv"}
    # companies_info_df: pd.DataFrame = pd.read_csv("/Users/mohamed/Desktop/data-projects/Jobs-Aggregator-Analyzer/app/pipeline/static/data/gold/companies_info.csv")
    # fortune_companies_df: pd.DataFrame = pd.read_csv("/Users/mohamed/Desktop/data-projects/Jobs-Aggregator-Analyzer/app/pipeline/static/data/gold/fortune_companies.csv")
    # fortune_companies_etl = FortuneCompaniesInfoETL(companies_info_df, fortune_companies_df, gold_storage_path)
    # fortune_companies_etl.run()
    
    # bronze_storage_path = staging_storage_path % {"file_name":"factless_fact_table.csv"}
    # gold_storage_path = production_storage_path % {"file_name":"factless_fact_table.csv"}
    # jobs_dim_df = pd.read_csv("data/gold/jobs.csv")
    # dates_dim_df = pd.read_csv("data/gold/dates.csv")
    # locations_dim_df = pd.read_csv("data/gold/locations.csv")
    # companies_dim_df = pd.read_csv("data/gold/companies.csv")
    # factless_fact_table_etl = FactlessFactTableETL(jobs_dim_df, dates_dim_df, locations_dim_df, companies_dim_df, bronze_storage_path, gold_storage_path)
    # factless_fact_table_etl.run()
    
    
    

if __name__ == "__main__":
    CONFIGS_PATH = "app/pipeline/settings/pipeline_configs.yaml"
    pipeline_configs: dict = Utils.get_configs(CONFIGS_PATH)

    LIGHTCAST_CLIENT_ID: str = os.getenv("LIGHTCAST_CLIENT_ID")
    LIGHTCAST_SECRET: str = os.getenv("LIGHTCAST_SECRET")
    LIGHTCAST_SCOPE: str = os.getenv("LIGHTCAST_SCOPE")
    LIGHTCAST_GRANT_TYPE: str = os.getenv("LIGHTCAST_GRANT_TYPE")
    LIGHTCAST_CREDENTIALS = LightCastCredentials(LIGHTCAST_CLIENT_ID,LIGHTCAST_SECRET,LIGHTCAST_GRANT_TYPE,LIGHTCAST_SCOPE)

    # COMPANIES_API_TOKEN: str = os.getenv("COMPANIES_API_TOKEN")
    COMPANIES_API_TOKEN: str = "QgqLYe9a"
    job_title, countries, pages_no = "data+engineer", None, 1
    start_date = "2021-01-01"
    end_date = "2050-12-31"
    job_params = {"pipeline_configs":pipeline_configs,"countries":countries,
                  "job_title":job_title,"pages_no": pages_no,
                  "lightcast_credentials": LIGHTCAST_CREDENTIALS,
                  "companies_api_token": COMPANIES_API_TOKEN,
                  "start_date": start_date, "end_date": end_date}
    
    asyncio.run(main(job_params))

