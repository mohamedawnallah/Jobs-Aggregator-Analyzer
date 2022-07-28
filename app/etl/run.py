"""Main Module of the application

Running ETL of the data from the multiple websites and storing it into a DWH
for further analytics and visualization.
"""
import json
from typing import Iterator
from loguru import logger
from etl.utils.utils import Utils
from etl.scrappers.indeed_scrapper import IndeedScrapper
from etl.etls.indeed_etl import IndeedETL
from models.job_models import Country
from etl.apis.job_skills_api import JobSkillsAPI

def main(params: dict):
    """Main entrypoint for ETLs across different scrappers"""
    configs,customized_countries,job_title,csv_file_path = params["configs"], params["customized_countries"],\
                                                           params["job_title"], params["csv_file_path"]
    pages_no: int = params["pages_no"]
    job_skills: str = params["job_skills"]
    indeed_etl = IndeedETL(configs,job_title,customized_countries,
                           pages_no, job_skills,csv_file_path)
    indeed_etl.run()

if __name__ == "__main__":
    # Preparing the configurations
    configs_path = "app/etl/settings/etl_configs.yaml"
    configs: dict = Utils.get_configs(configs_path)
    indeed_data_source = configs["data_sources"]["indeed"]
    countries_base_url: str = indeed_data_source["countries_base_url"]
    jobs_base_url: str = indeed_data_source["jobs_base_url"]
    job_base_url: str = indeed_data_source["job_base_url"]
    company_base_url: str = indeed_data_source["company_base_url"]

    job_title = "data engineer"
    country_names = "United States"
    country_code = "www"
    pages_no = 10
    pages_no: int = int(pages_no)
    csv_file_path = f"app/etl/static/data/{job_title}_jobs.csv"

    customized_countries: Iterator[Country] = IndeedScrapper.get_customized_indeed_countries(country_names,country_code)
    job_skills_api = JobSkillsAPI()
    job_skills: str = job_skills_api.get_latest_job_skills()
    job_params = {"configs":indeed_data_source,"customized_countries":customized_countries,
                  "job_title":job_title,"pages_no": pages_no,"csv_file_path":csv_file_path,
                  "job_skills":job_skills}
    main(job_params)

