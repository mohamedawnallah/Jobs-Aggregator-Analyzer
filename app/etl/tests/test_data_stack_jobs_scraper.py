""" Test Data Stack Jobs Scraper Module

This module tests all the functionalities of the DataStackJobsScraper class.
"""

import os
import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def data_stack_jobs_html(configs):
    """Fixture for retrieving sample Datastackjobs.com sample HTML file."""
    data_stack_jobs_html = configs["datastackjobs"]["data_stack_jobs_sample_html"]
    with open(data_stack_jobs_html, mode="r") as file:
        file_contents = file.read()
        return file_contents

def test_data_stack_jobs_html_fixture_configs_path(configs):
    html_path = configs["datastackjobs"]["data_stack_jobs_sample_html"]
    assert html_path == "app/etl/tests/resources/test_utils/data_stack_jobs_sample.html"

def test_data_stack_jobs_html_fixture_file_type_is_html(configs):
    html_path = configs["datastackjobs"]["data_stack_jobs_sample_html"]
    assert os.path.isfile(html_path)

def test_DataStackJobsScraper_URL(data_stack_jobs_scraper):
    scraper = data_stack_jobs_scraper
    assert scraper.url == "https://www.datastackjobs.com"

def test_access_job_data_return_type_is_list_of_dicts(data_stack_jobs_html, data_stack_jobs_scraper):
    scraper = data_stack_jobs_scraper
    html_contents = data_stack_jobs_html
    soup = BeautifulSoup(html_contents, "html.parser")
    jobs_data = scraper.access_job_data(soup)
    assert type(jobs_data) == list
    assert type(jobs_data[1]) == dict
    assert type(jobs_data[2]) == dict
