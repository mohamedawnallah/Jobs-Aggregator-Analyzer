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
    etl_configs, countries, job_title, csv_file_path = params["configs"], params["countries"], params["job_title"], params["csv_file_path"]
    pages_no: int = params["pages_no"]
    job_skills: str = params["job_skills"]
    indeed_etl_configs = etl_configs["data_sources"]["indeed"]
    
    indeed_etl = IndeedETL(indeed_etl_configs,job_title,countries,
                           pages_no, job_skills,csv_file_path)
    indeed_etl.run()

if __name__ == "__main__":
    # Preparing the configurations
    CONFIGS_PATH = "app/etl/settings/etl_configs.yaml"
    etl_configs: dict = Utils.get_configs(CONFIGS_PATH)
    indeed_etl_configs = etl_configs["data_sources"]["indeed"]
    lightcast_skills_configs: dict = etl_configs["data_sources"]["lightcast_skills"]
    job_title = "data engineer"
    country_name = "United States"
    country_code = "www"
    pages_no = 10
    csv_file_path = f"app/etl/static/data/{job_title}_jobs.csv"

    indeed_scrapper = IndeedScrapper(indeed_etl_configs,job_title)
    result = indeed_scrapper.get_countries(1)
    print(next(result))
    # countries: Iterator[Country] = IndeedScrapper.get_customized_indeed_country(country_name,country_code)
    # job_skills_api = JobSkillsAPI(lightcast_skills_configs)
    # job_skills: str = job_skills_api.get_latest_job_skills()
    # job_params = {"configs":indeed_etl_configs,"countries":countries,
    #               "job_title":job_title,"pages_no": pages_no,"csv_file_path":csv_file_path,
    #               "job_skills":job_skills}
                  
    # main(job_params)

