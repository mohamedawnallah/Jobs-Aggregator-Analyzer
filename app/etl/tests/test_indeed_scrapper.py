""" Test Indeed Scrapper Module

This module tests all the functionalities of the IndeedScrapper class.
"""
import os
from typing import Generator, Iterator, Optional, List
from dataclasses import is_dataclass
import responses
import pytest
from etl.scrappers.indeed_scrapper import IndeedScrapper
from models.job_dataclasses import Country


def test_get_indeed_countries(indeed_scrapper: IndeedScrapper) -> None:
    """Test the get_indeed_countries method"""
    countries: list[Country] = list(indeed_scrapper.get_countries(countries_no=1))
    country: Country = countries[0]
    assert len(countries) == 1
    assert is_dataclass(country)

@responses.activate
def test_get_mocked_indeed_countries(indeed_scrapper: IndeedScrapper) -> None:
    """Test Countries are returned"""
    countries_url = "https://www.indeed.com/worldwide"
    jobs_example_html_path: str = "app/etl/tests/resources/test_utils/indeed_countries_worldwide.html"
    with open(jobs_example_html_path, "r",encoding="utf-8") as fh:
        html = fh.read()
        responses.add(
            responses.GET,
            url=countries_url,
            body=html,
            status=200,
            content_type="text/html",
        )
    countries: Iterator[Country] = indeed_scrapper.get_countries(countries_no=10,countries_url=countries_url)
    countries: list[Country] = list(countries)
    country: Country = countries[0]
    expected_is_dataclass = True
    expected_length = 10
    assert is_dataclass(country) is expected_is_dataclass
    assert len(countries) == expected_length


# def test_get_pages_no(indeed_scrapper) -> None:
#     """Test Pages are returned"""
#     job_title = "data engineer"
#     job_title_url = job_title.replace(" ", "+")
#     country_code = "eg"
#     jobs_url = indeed_scrapper.jobs_base_url % {
#         "job_title": job_title_url,
#         "country_code": country_code,
#     }
#     max_page_no = indeed_scrapper.get_pages_no(jobs_url)
#     assert max_page_no > 0


# def test_get_results_job_cards_col(indeed_scrapper) -> None:
#     """Test Results are returned"""
#     jobs_url = "https://www.indeed.com/jobs?q=data+engineer&l=Egypt&start=0"
#     results = indeed_scrapper.get_results_job_cards_col(jobs_url)
#     assert results is not None


# def test_get_invalid_results_job_cards_col(indeed_scrapper) -> None:
#     """Test Results are returned"""
#     invalid_job_url = (
#         "https://www.indeed.codsadsam/invalid_jobs?q=data+engineer&l=Egypt&start=0"
#     )
#     with pytest.raises(InvalidUrlError) as invalid_url_error:
#         indeed_scrapper.get_results_job_cards_col(invalid_job_url)
#     assert invalid_url_error.value.args[0] == "Invalid URL"


# @pytest.mark.parametrize(
#     "job_title,countries,pages_no", [("data engineer", {"United States": "www"}, 1)]
# )
# def test_get_jobs_countries(
#     indeed_scrapper, job_title: str, countries: dict, pages_no: int
# ) -> None:
#     """Test Jobs Countries are returned"""
#     jobs_countries = indeed_scrapper.get_jobs_countries(countries, job_title, pages_no)
#     assert isinstance(jobs_countries, Generator)
#     assert isinstance(next(next(jobs_countries)), dict)


# @pytest.mark.parametrize(
#     "job_title,countries,pages_no", [("data engineer", {"Egypt": "eg"}, 1)]
# )
# def test_write_to_csv(
#     indeed_scrapper, configs, job_title: str, countries: dict, pages_no: int
# ) -> None:
#     """Test write_to_csv"""
#     jobs_countries = indeed_scrapper.get_jobs_countries(countries, job_title, pages_no)
#     csv_file_path = "tests/resources/test_indeed_scrapper.csv"
#     skills_config_name = "data_engineering_skills"
#     csv_header = Utils.get_csv_header(configs, skills_config_name)
#     IndeedScrapper.write_to_csv(csv_file_path, jobs_countries, csv_header)

#     assert os.path.exists(csv_file_path)


# if __name__ == "__main__":
#     pass
