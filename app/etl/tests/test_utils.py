""" Test Utils module 

Testing all the static methods of Utils class that are reused in other modules.
"""
# from http.client import responses
from typing import Iterator, Type
import pytest
import requests
from bs4 import BeautifulSoup
from etl.utils.utils import Utils

@pytest.mark.parametrize("text, expected_result", [
    ("", ""),
    ("\n", ""),
    ("INVALIDTEXT","invalidtext")
])
def test_get_valid_text(text: str, expected_result: str) -> None:
    """Test get_valid_text"""
    result = Utils.get_valid_text(text)
    assert result == expected_result

@pytest.mark.parametrize("text, expected_result", [
    ("INVALIDTEXT", "invalidtext"),
    ("INVALIDTEXT\n\n\n", "invalidtext"),
    (None, "N/A")
])
def test_get_valid_value(text: str, expected_result: str) -> None:
    """Test valid value is returned"""
    result = Utils.get_valid_value(text)
    assert result == expected_result

@pytest.mark.parametrize("text, expected_result", [
    ("1, 2, 3, 4, 5", [1, 2, 3, 4, 5]),
    ("2,123,235 31",[2123235, 31]),
])
def test_get_numbers_from_string(text,expected_result) -> None:
    """Test get_numbers_from_string"""
    result = Utils.get_numbers_from_string(text)
    assert result == expected_result

@pytest.mark.parametrize("search_word, text, expected_result", [
    ("python", "python is great", True),
    ("python", "pythons is great", False),
    ("java", "all programming languages're great", False),
])
def test_is_word_found(search_word: str, text: str, expected_result: bool) -> None:
    """Test is_word_found"""
    result = Utils.is_word_found(search_word, text)
    assert result is expected_result

@pytest.mark.parametrize("search_words, text, expected_result", [
    (["python", "java"], "python is great", False),
    (["python", "java"], "java is great", False),
    (["python", "java"], "python is great and java is great", True),
    (["python", "java"], "python is great and java is great and python is great", True),
    (["python", "java"], "all programming languages're great", False),
])
def test_are_all_words_found(search_words: list[str], text: str, expected_result: bool) -> None:
    """Test are_words_found"""
    result = Utils.are_all_words_found(search_words, text)
    assert result is expected_result

def test_get_configs() -> None:
    """Test get_configs"""
    configs_path = "app/etl/settings/etl_configs.yaml"
    configs = Utils.get_configs(configs_path)
    expected_result = dict
    assert isinstance(configs, expected_result)


    
# @responses.activate
# def test_get_page_parsed() -> None:
#     """Ensure that indeed jobs html example is parsed correctly"""
#     url = "https://www.indeed.com/invalid/jobs?q=Data%20Engineering"
#     jobs_example_html_path: str = "app/etl/tests/resources/test_utils/indeed_jobs_example.html"
#     with open(jobs_example_html_path, "r",encoding="utf-8") as fh:
#         html = fh.read()
#         responses.add(
#             responses.GET,
#             url=url,
#             body=html,
#             status=200,
#             content_type="text/html",
#         )
#     expected_result = BeautifulSoup
#     page_parsd: BeautifulSoup = Utils.get_page_parsed(url)
#     assert isinstance(page_parsd, expected_result)