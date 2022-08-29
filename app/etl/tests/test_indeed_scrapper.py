""" Test Indeed Scrapper Module

This module tests all the functionalities of the IndeedScrapper class.
"""
from typing import Generator, Iterator, Optional, List
from unittest.mock import patch, MagicMock
import pytest
import bs4

from etl.scrappers.indeed_scrapper import IndeedScrapper
from etl.utilities.utils import Utils
from etl.models.job_models import CompanyBasicInfo, Country, JobBasicInfo, JobFullInfo

def test_get_indeed_countries(indeed_scrapper: IndeedScrapper) -> None:
    """Test the get_indeed_countries"""
    countries_no = 1
    countries_result = indeed_scrapper.get_countries(countries_no)
    country = next(countries_result)
    assert country is not None

def test_get_mocked_indeed_countries(indeed_scrapper: IndeedScrapper) -> None:
    """Test Countries are returned"""
    countries_url = "https://www.indeed.com/worldwide"
    indeed_countries_worldwide_path: str = "app/etl/tests/resources/test_indeed_etl/indeed_countries_worldwide.html"
    with open(indeed_countries_worldwide_path, "r",encoding="utf-8") as fh:
        indeed_countries_html: str = fh.read()
    with patch("etl.utils.utils.Utils.get_html_page", MagicMock(return_value=indeed_countries_html)):
        countries: Generator[Country] = indeed_scrapper.get_countries(countries_no=10,countries_url=countries_url)
        countries: List[Country] = list(countries)
        expected_countries_length = 10
        assert len(countries) == expected_countries_length

def test_get_pages_no(indeed_scrapper: IndeedScrapper) -> None:
    """Test the get_pages_no"""
    country_jobs_url = "https://www.indeed.com/jobs?q=python&l=United+States"
    max_page_no = indeed_scrapper.get_pages_no(country_jobs_url)
    assert max_page_no >= 1

def test_get_mocked_pages_no(indeed_scrapper: IndeedScrapper) -> None:
    """Test the get_pages_no"""
    country_jobs_url="https://www.indeed.com/jobs?q=python&l=United+States"
    jobs_html_example_path: str = "app/etl/tests/resources/test_indeed_etl/indeed_last_page_jobs_example.html"
    with open(jobs_html_example_path, "r",encoding="utf-8") as fh:
        jobs_html: str = fh.read()
    jobs_soup = Utils.get_beautiful_soup(jobs_html)
    with patch("etl.scrappers.indeed_scrapper.IndeedScrapper.get_results_job_cards_collection", MagicMock(return_value=jobs_soup)):
        max_page_no = indeed_scrapper.get_pages_no(country_jobs_url)
        expected_max_page_no = 65
        assert max_page_no == expected_max_page_no
    
def test_get_results_job_cards_collection(indeed_scrapper: IndeedScrapper) -> None:
    """Test the get_results_job_cards_collection"""
    country_jobs_url="https://www.indeed.com/jobs?q=python&l=United+States"
    jobs_html_example_path: str = "app/etl/tests/resources/test_indeed_etl/indeed_first_page_jobs_example.html"
    with open(jobs_html_example_path, "r",encoding="utf-8") as fh:
        jobs_html: str = fh.read()
    jobs_soup = Utils.get_beautiful_soup(jobs_html)
    with patch("etl.scrappers.indeed_scrapper.Utils.get_page_parsed", MagicMock(return_value=jobs_soup)):
        job_cards_result = indeed_scrapper.get_results_job_cards_collection(country_jobs_url)
    assert job_cards_result is not None

def test_get_customized_indeed_country() -> None:
    """Test the get_customized_indeed_country"""
    country_name = "United States"
    country_code = "wwww"
    country: Generator[Country] = IndeedScrapper.get_customized_indeed_country(country_name, country_code)
    assert country is not None

@pytest.mark.parametrize("country_name, country_code, job_title, pages_no", [
    ("United States", "wwww", "Data Engineer", 1),
    ("United Kingdom", "uk", "Python Developer", 1),
])
def test_get_jobs_countries(indeed_scrapper: IndeedScrapper, country_name, country_code, job_title, pages_no) -> None:
    """Test the get_jobs_countries"""
    country: Generator[Country,None,None] = IndeedScrapper.get_customized_indeed_country(country_name, country_code)
    jobs_countries = indeed_scrapper.get_jobs_countries(country,job_title,pages_no)
    country_jobs_url, max_page_no, country_name = next(jobs_countries)
    assert country_jobs_url is not None and max_page_no is not None and country_name is not None

@pytest.mark.parametrize("country_jobs_url, max_page_no", [
    ("https://www.indeed.com/jobs?q=python&l=United+States", 1),
])
def test_get_jobs_for_each_page(indeed_scrapper: IndeedScrapper, country_jobs_url, max_page_no) -> None:
    """Test the get_jobs_countries"""
    jobs_html_example_path: str = "app/etl/tests/resources/test_indeed_etl/indeed_first_page_jobs_example.html"
    with open(jobs_html_example_path, "r",encoding="utf-8") as fh:
        jobs_html: str = fh.read()
    jobs_soup = Utils.get_beautiful_soup(jobs_html)
    with patch("etl.scrappers.indeed_scrapper.IndeedScrapper.get_results_job_cards_collection", MagicMock(return_value=jobs_soup)):
        jobs_raw_page: bs4.element.ResultSet = indeed_scrapper.get_jobs_for_each_page(country_jobs_url,max_page_no)
    assert isinstance(next(jobs_raw_page), bs4.element.ResultSet)

@pytest.mark.parametrize("country_jobs_url, max_page_no", [
    ("https://www.indeed.com/jobs?q=python&l=United+States", 1),
])
def test_get_basic_job_info(indeed_scrapper: IndeedScrapper, country_jobs_url, max_page_no) -> None:
    """Test the get_basic_job_info"""
    jobs_html_example_path: str = "app/etl/tests/resources/test_indeed_etl/indeed_first_page_jobs_example.html"
    with open(jobs_html_example_path, "r",encoding="utf-8") as fh:
        jobs_html: str = fh.read()
    jobs_soup = Utils.get_beautiful_soup(jobs_html)
    with patch("etl.scrappers.indeed_scrapper.IndeedScrapper.get_results_job_cards_collection", MagicMock(return_value=jobs_soup)):
        jobs_raw_page: Generator[bs4.element.ResultSet] = indeed_scrapper.get_jobs_for_each_page(country_jobs_url,max_page_no)
        first_jobs_page_raw: bs4.element.ResultSet = next(jobs_raw_page)
        country_name = "United States"
        basic_job_info: Generator[tuple[JobBasicInfo,CompanyBasicInfo],None,None] = indeed_scrapper.get_basic_job_info(first_jobs_page_raw,country_name) 
        job_basic_info, company_basic_info = next(basic_job_info)
    assert job_basic_info is not None and company_basic_info is not None

@pytest.mark.parametrize("country_jobs_url, max_page_no", [
    ("https://www.indeed.com/jobs?q=python&l=United+States", 1),
])
def test_get_more_job_info(indeed_scrapper: IndeedScrapper, country_jobs_url, max_page_no) -> None:
    """Test Get More Job Info"""
    jobs_html_example_path: str = "app/etl/tests/resources/test_indeed_etl/indeed_first_page_jobs_example.html"
    job_full_info_html_example_path: str = "app/etl/tests/resources/test_indeed_etl/indeed_job_full_info_example.html"
    with open(jobs_html_example_path, "r",encoding="utf-8") as jobs_html_fh:
        jobs_html: str = jobs_html_fh.read()
    with open(job_full_info_html_example_path, "r",encoding="utf-8") as jobs_full_info_html_fh:
        jobs_full_info_html: str = jobs_full_info_html_fh.read()  
    jobs_soup = Utils.get_beautiful_soup(jobs_html)
    job_full_info_soup = Utils.get_beautiful_soup(jobs_full_info_html)
    with patch("etl.scrappers.indeed_scrapper.IndeedScrapper.get_results_job_cards_collection", MagicMock(return_value=jobs_soup)):
        jobs_raw_page: Generator[bs4.element.ResultSet] = indeed_scrapper.get_jobs_for_each_page(country_jobs_url,max_page_no)
        first_jobs_page_raw: bs4.element.ResultSet = next(jobs_raw_page)
        country_name = "United States"
        basic_job_info: Generator[tuple[JobBasicInfo,CompanyBasicInfo],None,None] = indeed_scrapper.get_basic_job_info(first_jobs_page_raw,country_name) 
        job_basic_info, company_basic_info = next(basic_job_info)
    with patch("etl.scrappers.indeed_scrapper.Utils.get_page_parsed", MagicMock(return_value=job_full_info_soup)):
        job_full_info: JobFullInfo = indeed_scrapper.get_more_job_info(job_basic_info, company_basic_info)
    assert job_full_info is not None
