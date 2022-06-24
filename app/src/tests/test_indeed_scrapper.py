
import sys
import os
from typing import Generator

# append the src parent directory to sys path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import toml
from scrappers.indeed_scrapper import IndeedScrapper
from utils.constants import CONFIGS_PATH
from utils.helpers import InvalidUrlError
from utils.helpers import Utils

@pytest.fixture
def configs() -> dict:
    """Fixture for configs"""
    return toml.load(CONFIGS_PATH)

@pytest.fixture
def indeed_scrapper(configs):
    """Fixture for IndeedScrapper"""
    skills_config_name = 'data_engineering_skills'
    return IndeedScrapper(configs,skills_config_name)

def test_get_indeed_countries(indeed_scrapper: IndeedScrapper):
    """Test Countries are returned"""
    countries = indeed_scrapper.get_countries(end_pos=10)
    assert len(countries) > 0
    assert isinstance(countries, dict)

def test_get_pages_no(indeed_scrapper: IndeedScrapper):
    """Test Pages are returned"""
    job_title = 'data engineer'
    job_title_url = job_title.replace(' ','+')
    country_code = 'eg'
    jobs_url = indeed_scrapper.jobs_base_url % {'job_title':job_title_url,'country_code':country_code}
    max_page_no = indeed_scrapper.get_pages_no(jobs_url)
    assert max_page_no > 0

def test_get_results_job_cards_col(indeed_scrapper: IndeedScrapper):
    """Test Results are returned"""
    jobs_url = 'https://www.indeed.com/jobs?q=data+engineer&l=Egypt&start=0'
    results = indeed_scrapper.get_results_job_cards_col(jobs_url)
    assert results is not None

def test_get_invalid_results_job_cards_col(indeed_scrapper: IndeedScrapper):
    """Test Results are returned"""
    invalid_job_url = 'https://www.indeed.codsadsam/invalid_jobs?q=data+engineer&l=Egypt&start=0'
    with pytest.raises(InvalidUrlError):
        indeed_scrapper.get_results_job_cards_col(invalid_job_url)

def test_get_jobs_countries(indeed_scrapper: IndeedScrapper):
    countries_input = {'United States':'www'}
    job_title_input = 'Data Engineer'
    pages_no = 1

    jobs_countries = indeed_scrapper.get_jobs_countries(countries_input,job_title_input,pages_no)
        
    assert isinstance(jobs_countries, Generator)
    first_job_country = next(next(jobs_countries))
    assert isinstance(first_job_country, dict)

def test_write_to_csv(indeed_scrapper,configs: dict):
    """Test write_to_csv"""
    countries_input = {'United States':'www'}
    job_title_input = 'Data Engineer'
    pages_no = 1
    jobs_countries_gen = indeed_scrapper.get_jobs_countries(countries_input,job_title_input,pages_no)
    csv_file_path = 'tests/resources/test_indeed_scrapper.csv'
    skills_config_name = 'data_engineering_skills'
    csv_header = Utils.get_csv_header(configs,skills_config_name)
    IndeedScrapper.write_to_csv(csv_file_path,jobs_countries_gen,csv_header)
    #check that file generated at tests/resources/test_indeed_scrapper.csv
    assert os.path.exists(csv_file_path)

if __name__ == '__main__':
    pytest.main()