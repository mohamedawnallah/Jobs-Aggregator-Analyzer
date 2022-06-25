""" Test Utils module 

Testing all the static methods of Utils class that are reused in other modules.
"""
import os
import pytest
import requests
from bs4 import BeautifulSoup
from utils.helpers import Utils
from utils.helpers import CSVHeaderError, InvalidUrlError

@pytest.fixture
def configs() -> dict:
    """Fixture for configs"""
    return Utils.get_configs("settings/configs.toml")

def test_get_valid_value():
    """Test valid value is returned"""
    assert Utils.get_valid_value(None) == 'N/A'

def test_words_are_found():
    """Test is_word_found"""
    search_words = ['Bachelor']
    text = 'bachelor'
    assert Utils.are_words_found(search_words, text) is True

def test_words_are_not_found():
    """Test word is not found"""
    search_words = ['Bachelor']
    text = 'High School'
    assert Utils.are_words_found(search_words, text) is False

def test_needs_cs_degree():
    """Test check_degree"""
    search_words = ['Computer Science','Bachelor']
    text = 'bachelor computer science'
    assert Utils.check_degree(search_words, text) is True

def test_does_not_need_cs_degree():
    """Test check_degree"""
    search_words = ['Computer Science','Bachelor']
    text = 'skills 1. 2. 3. 4. proactive person'
    assert Utils.check_degree(search_words, text) is False

def test_get_matched_skills(configs):
    """Test get_matched_skills"""
    root_info_data = 'data engineering needs apache airflow and python'
    job_skills_config = configs['data_engineering_skills']
    matched_skills: dict = Utils.get_matched_skills(job_skills_config, root_info_data) 
    assert matched_skills['programming_languages'] != 'N/A'
    assert matched_skills['orcherstration'] != 'N/A'

def test_get_non_matched_skills(configs):
    """Test get_non_matched_skills"""

    root_info_data = 'data engineering needs invalid and invalid'
    job_skills_config = configs['data_engineering_skills']
    non_matched_skills: dict = Utils.get_matched_skills(job_skills_config, root_info_data) 
    assert non_matched_skills['programming_languages'] == 'N/A'
    assert non_matched_skills['orcherstration'] == 'N/A'

def test_get_valid_page_parsed():
    """Test get_page_parsed"""
    valid_url = 'https://www.indeed.com/jobs?q=data+engineering&l=New+York%2C+NY'
    jobs_response = requests.get(valid_url)
    jobs_soup = BeautifulSoup(jobs_response.text, 'html.parser')
    assert jobs_soup is not None

def test_get_invalid_page_parsed():
    """Test get_page_parsed"""
    invalid_url = 'https://www.indeed.dsadsa/invalid_jobs?q=data+engineering&l=New+York%2C+NY'
    with pytest.raises(InvalidUrlError):
        Utils.get_page_parsed(invalid_url)

def test_get_csv_header(configs):
    """Test get_csv_header"""
    skills_name_config = 'data_engineering_skills'
    header = Utils.get_csv_header(configs,skills_name_config)
    assert header is not None
    assert isinstance(header, list)

def test_get_error_csv_header(configs):
    """Test get_csv_header"""
    skills_name_config = {'skills':['data engineering']}
    # assert that exception is raised
    with pytest.raises(CSVHeaderError):
        Utils.get_csv_header(configs,skills_name_config)

def test_get_valid_value_key_from_dict():
    """Test get_values_from_dict"""
    data = {'a':1,'b':2,'c':{'d':3,'e':4}}
    values = Utils.get_value_key_attr(data,'c')
    assert values == {'d':3,'e':4}

def test_get_invalid_value_key_from_dict():
    """Test get_values_from_dict"""
    data = {'a':1,'b':2,'c':{'d':3,'e':4}}
    values = Utils.get_value_key_attr(data,'f')
    assert values is None

if __name__ == '__main__':
    pass