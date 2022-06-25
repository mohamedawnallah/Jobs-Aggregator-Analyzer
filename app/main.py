"""Main Module of the application

Running ETL of the data from the multiple websites and storing it into a DWH
for further analytics and visualization.
"""
from utils.helpers import Utils
from scrappers.indeed_scrapper import IndeedScrapper
import pytest

def main():
    """Main function
    
    Entry point to trigger the ETL process for jobs.
    """
    configs_path = 'settings/configs.toml'
    configs: dict = Utils.get_configs(configs_path)
    skills_config_name = 'data_engineering_skills'
    job_title_input = 'Data Engineer'
    csv_file_path = f"static/data/{job_title_input}_jobs.csv"
    csv_header = Utils.get_csv_header(configs,skills_config_name)

    scrapper = IndeedScrapper(configs,skills_config_name)
    countries = scrapper.get_countries()
    jobs_gen = scrapper.get_jobs_countries(countries,job_title_input)
    IndeedScrapper.write_to_csv(csv_file_path,jobs_gen,csv_header)

if __name__ == '__main__':
    pass
