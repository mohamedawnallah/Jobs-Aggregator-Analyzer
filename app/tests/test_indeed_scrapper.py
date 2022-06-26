""" Test Indeed Scrapper Module

This module tests all the functionalities of the IndeedScrapper class.
"""
import os
from typing import Generator
import pytest
from scrappers.indeed_scrapper import IndeedScrapper
from utils.helpers import InvalidUrlError
from utils.helpers import Utils

@pytest.fixture
def configs() -> dict:
    """Fixture for configs"""
    return Utils.get_configs("settings/configs.toml")

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

dummy_data = [('data engineer',{"United States":'www'},1)]
@pytest.mark.parametrize('job_title,countries,pages_no',dummy_data)
def test_get_jobs_countries(indeed_scrapper: IndeedScrapper, job_title: str,
                            countries: dict, pages_no: int):
    """Test Jobs Countries are returned"""
    jobs_countries = indeed_scrapper.get_jobs_countries(countries,job_title,pages_no)
    assert isinstance(jobs_countries, Generator)
    assert isinstance(next(next(jobs_countries)), dict)


@pytest.mark.parametrize('job_title,countries,pages_no',dummy_data)
def test_write_to_csv(indeed_scrapper: IndeedScrapper, configs: dict,
                      job_title: str, countries: dict, pages_no: int):
    """Test write_to_csv"""
    jobs_countries = indeed_scrapper.get_jobs_countries(countries,job_title,pages_no)
    csv_file_path = 'tests/resources/test_indeed_scrapper.csv'
    skills_config_name = 'data_engineering_skills'
    csv_header = Utils.get_csv_header(configs,skills_config_name)
    IndeedScrapper.write_to_csv(csv_file_path,jobs_countries,csv_header)
    
    assert os.path.exists(csv_file_path)

if __name__ == '__main__':
    pass