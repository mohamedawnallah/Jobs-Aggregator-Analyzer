"""Main Module of the application

Running ETL of the data from the multiple websites and storing it into a DWH
for further analytics and visualization.
"""
from typing import Iterator
import json
import logging
import sys
import logging.config
from loguru import logger
from etl.utils.utils import Utils
from etl.scrappers.indeed_scrapper import IndeedScrapper
from etl.etls.indeed_etl import IndeedETL
from etl.models.job_dataclasses import Country
from etl.utils.job_specifications import (
    JobDescriptionFilter,
    MasterComputerScienceSpecification,
    OrSpecification,
    PHDComputerScienceSpecification,
    ProgrammingLanguagesSpecification,
    IngestTechSpecification,
    CloudProvidersSpecification,
    MetaStoreSpecification,
    OpenTableFormatsSpecification,
    DevopsSpecification,
    AutomationSpecification,
    AnalyticsEngineSpecification,
    ObjectStorageSpecification,
    SQLSpecification,
    OrcherstrationSpecification,
    DataVizToolsSpecification,
    DiscoveryGovernanceSpecification,
    MlopsEndtoEndSpecification,
    BachelorComputerScienceSpecification,

)
def main(configs:dict, job_title:str, job_skills:OrSpecification, csv_file_path: str, customized_countries:Iterator[Country]=None, countries_no:int=None, jobs_pages_no:int=None):
    """Main entrypoint for ETLs across different scrappers"""
    indeed_etl = IndeedETL(configs, job_title, job_skills)
    job_items_generator: Iterator[dict] = indeed_etl.extract(customized_countries=customized_countries, countries_no=countries_no, jobs_pages_no=jobs_pages_no)
    indeed_etl.load(csv_file_path=csv_file_path, jobs_countries=job_items_generator)
    



if __name__ == "__main__":
    configs_path = "app/etl/settings/configs.toml"
    configs: dict = Utils.get_configs(configs_path)
    job_title = "data engineer"
    countries: Iterator[Country] = IndeedScrapper.get_customized_indeed_country(country_name="United States",country_code="www")
    job_skills = (
        ProgrammingLanguagesSpecification(configs)
        | IngestTechSpecification(configs)
        | CloudProvidersSpecification(configs)
        | MetaStoreSpecification(configs)
        | OpenTableFormatsSpecification(configs)
        | DevopsSpecification(configs)
        | AutomationSpecification(configs)
        | AnalyticsEngineSpecification(configs)
        | ObjectStorageSpecification(configs)
        | SQLSpecification(configs)
        | OrcherstrationSpecification(configs)
        | DataVizToolsSpecification(configs)
        | DiscoveryGovernanceSpecification(configs)
        | MlopsEndtoEndSpecification(configs)
        | BachelorComputerScienceSpecification()
    )
    logger.add("app/etl/logs/debug.log",level="DEBUG",rotation="500 MB")
    logger.add("app/etl/logs/warning.log",level="WARNING")
    logger.add("app/etl/logs/error.log",level="ERROR")
    logger.add("app/etl/logs/critical.log",level="CRITICAL")
    csv_file_path = f"app/etl/static/data/{job_title}_jobs.csv"
    main(configs=configs, job_title=job_title, job_skills=job_skills,customized_countries=countries,csv_file_path=csv_file_path)



