"""Helpers module needed through out the application

Reusable functions that are used throughout the application from different modules
"""
import re
from abc import ABC, abstractmethod
from typing import Optional, Union, Generator, Any, Iterator
from collections import namedtuple, defaultdict
import requests
import toml
import bs4
from bs4 import BeautifulSoup
from loguru import logger

class Utils:
    """Utils Class"""

    @staticmethod
    def get_valid_value(value: Union[bs4.element.Tag, str]) -> str:
        """Handling Null values in indeed jobs"""
        if value is None:
            return "N/A"
        is_bs4_tag = isinstance(value, bs4.element.Tag)
        if is_bs4_tag:
            text = Utils.get_valid_text(value.text)
            return text
        text = Utils.get_valid_text(value)
        return text

    @staticmethod
    def get_valid_text(description: str) -> str:
        """Handling text format"""
        text = description.replace("\n", " ").lower().strip()
        text = text.replace(",", " ")
        return text

    @staticmethod
    def get_numbers_from_string(text: str) -> list[int]:
        """Get number from string"""
        text = text.replace(',', '')
        return [int(s) for s in text.split() if s.isdigit()]

    @staticmethod
    def are_all_words_found(search_words: list[str], text):
        """Check if all the whole words is found in the given text"""
        text = Utils.get_valid_text(text)
        for search_word in search_words:
            is_word_found = Utils.is_word_found(search_word, text)
            if not is_word_found:
                return False
        return True

    @staticmethod
    def is_word_found(search_word: str, text: str) -> bool:
        """Check if the word is found in the given text"""
        search_word = Utils.get_valid_text(search_word)
        text = Utils.get_valid_text(text)
        if not re.search(r"\b" + re.escape(search_word) + r"\b", text):
            return False
        return True

    @staticmethod
    def get_page_parsed(url: str) -> BeautifulSoup:
        """Get beautiful soup for the given link"""
        while True:
            try:
                jobs_response = requests.get(url)
                break
            except requests.exceptions.ConnectionError as connection_error:
                logger.warning(connection_error)
                continue
            except requests.exceptions.MissingSchema as missing_schema_error:
                logger.error(missing_schema_error)
        jobs_soup: bs4.BeautifulSoup = BeautifulSoup(jobs_response.text, "html.parser")
        return jobs_soup

    @staticmethod
    def get_configs(configs_path: str = "app/etl/settings/configs.toml") -> dict:
        """Get the configs from the config file"""
        configs = toml.load(configs_path)
        return configs

    @staticmethod
    def get_value_of_key_from_dict(configs_input: dict, key: str):
        """Get the value of the key from the configs"""
        if key in configs_input:
            return configs_input[key]
        for values in configs_input.values():
            if key in values:
                return Utils.get_value_of_key_from_dict(values,key)
        return None
    
    @staticmethod
    def is_job_spec_satisfied(
        job_specs_values: list[str], job_spec: str, job_description: str
    ) -> Iterator[dict]:
        """Check if the job spec is satisfied by the candidate(job description)"""
        yielded = False
        for job_spec_value in job_specs_values:
            is_job_spec_found = Utils.is_word_found(job_spec_value, job_description)
            if is_job_spec_found:
                yielded = True
                yield {job_spec: job_spec_value}
        if not yielded:        
            yield {job_spec: "N/A"}


    @staticmethod
    def is_degree_filter_satisfied(
        job_spec: str, degree_filter: list[str], job_description: str
    ) -> Iterator[dict]:
        """Check if job needs computer science degree (as long as) our main concern now is in Data/SE jobs"""
        is_degree_filter_satisfied =  Utils.are_all_words_found(degree_filter, job_description)
        if is_degree_filter_satisfied:
            yield {job_spec: str(is_degree_filter_satisfied)}
        else:
            yield {job_spec: str(is_degree_filter_satisfied)}


    @staticmethod
    def are_all_job_skills_null(job_skills: dict[str]) -> bool:
        """Check if all the job skills are null"""
        for job_skill in job_skills.values():
            if not job_skill.startswith("N/A"):
                return False
        return True