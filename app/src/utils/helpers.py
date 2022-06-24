from abc import ABC, abstractmethod
from collections import namedtuple
from collections import defaultdict
from typing import Optional, Union
import re
import json
import toml
import bs4

import requests

from bs4 import BeautifulSoup
from utils.constants import CONFIGS_PATH


class Scrapper(ABC):
    """Scrapper Abstract Class for other Web Scrappers"""
    @abstractmethod
    def get_countries(self, end_pos: Optional[int] = None) -> dict:
        """Get the list of countries supported by indedd"""
        pass
    
    @abstractmethod
    def get_jobs_countries(self, countries_input: dict, job_title_input: str, page_no: Optional[int] = None):
        """Get jobs depending on the website also the passed job title"""
        pass

    @abstractmethod
    def get_pages_no(self, jobs_url: str) -> int:
        """Get pages number per page depending on business logic of the website"""
        pass

    @staticmethod
    @abstractmethod
    def write_to_csv(csv_file_name: str, jobs: object, csv_headers: list) -> None:
        """Write jobs to csv file"""
        pass

class DegreeChecker(ABC):
    """Abstract Class for Degree Checker"""
    @abstractmethod
    def check_degree(self, degree_filter: list[str], text: str) -> bool:
        """Check if the job title has degree"""
        pass

class Utils(DegreeChecker):
    """Utils Class"""

    @staticmethod      
    def get_valid_value(value: Union[bs4.element.Tag, str]) -> str:
        """Handling Null values in indeed jobs"""
        if value is None:
            return "N/A"
            
        is_bs4_tag = isinstance(value, bs4.element.Tag)
        if is_bs4_tag:
            return value.text.strip()
        return value.strip()

    @staticmethod
    def check_degree(degree_filter:list[str] , text:str) -> bool:
        """Check if job needs computer science degree (as long as) our main concern now is in Data/SE jobs"""
        if Utils.is_word_found(degree_filter, text):
            return True
        return False

    @staticmethod
    def is_word_found(search_words: list[str], text):
        """Check if the whole word is found in the given text"""
        matched = False
        for search_word in search_words:    
            search_word = search_word.lower()        
            if re.search(r"\b" + re.escape(search_word) + r"\b", text):
                matched = True
            else:
                matched = False
        return matched
    
    @staticmethod
    def get_matched_skills(job_skills_config: dict, root_info_data: str):
        """Match job skills mentioned with ones in config file"""
        job_skills_dict = defaultdict(str) 

        for key,values in job_skills_config.items():
            for value in values:
                if Utils.is_word_found([value],root_info_data):
                    print(value)
                    job_skills_dict[key] += value + ', '
                
            if key not in job_skills_dict:
                job_skills_dict[key] = "N/A"
        
        return job_skills_dict 

    @staticmethod
    def get_page_parsed(url: str) -> BeautifulSoup:
        """Get beautiful soup for the given link"""
        try:
            jobs_response = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            raise InvalidUrlError(url)
        jobs_soup = BeautifulSoup(jobs_response.text, 'html.parser')
        return jobs_soup


    # def get_configs(self) -> dict:
    #     """Get configs from config file"""
    #     configs = toml.load(CONFIGS_PATH)
    #     return configs
    @staticmethod
    def get_csv_header(main_configs : dict, skills_name_config: str) -> list[str]:
        """Get csv header"""
        if not isinstance(skills_name_config, str):
            raise CSVHeaderError("Skill name config must be a string refers to the corresponding one in the config file (skills section)")

        company_info = Utils.get_value_key_attr(main_configs, 'company')
        job_attrs_info = Utils.get_value_key_attr(main_configs, 'job')
        job_basic_info = Utils.get_value_key_attr(job_attrs_info, 'basic_info')
        job_additional_info = Utils.get_value_key_attr(job_attrs_info, 'additional_info')
        job_skills = Utils.get_value_key_attr(main_configs, skills_name_config)


        company_info_keys = list(company_info.keys())
        job_basic_info_keys = list(job_basic_info.keys())
        job_additional_info_keys = list(job_additional_info.keys())
        job_skills_keys = list(job_skills.keys())

        csv_header = job_basic_info_keys + job_additional_info_keys + company_info_keys + job_skills_keys
        return csv_header

    @staticmethod
    def get_value_key_attr(configs_input: dict,key:str) -> dict:
        """Get values of key given key attribute from config file regards to 
        the job info, company info, data engineering skills and more"""
        
        if key in configs_input: return configs_input[key]
        for k,v in configs_input.items():
            if isinstance(v,dict):
                return Utils.get_value_key_attr(v,key)


class InvalidUrlError(Exception):
    """Invalid Url Custom Exception"""
    # add custom message
    def __init__(self, message):
        """Initialize the exception with custom message"""
        super().__init__(message)

class CSVHeaderError(Exception):
    """CSV Header Custom Exception"""
    # add custom message
    def __init__(self, message):
        """Initialize the exception with custom message"""
        super().__init__(message)


configs = toml.load(CONFIGS_PATH)
company_attrs: dict = Utils.get_value_key_attr(configs,'company')
job_attrs: dict = Utils.get_value_key_attr(configs,'job')
job_basic_info_attrs: dict = Utils.get_value_key_attr(job_attrs,'basic_info')
job_additional_info_attrs: dict = Utils.get_value_key_attr(job_attrs,'additional_info')

print(job_basic_info_attrs)
company_attrs_list: list = list(company_attrs.keys())
job_basic_info_attrs_list: list = list(job_basic_info_attrs.keys())
job_additional_info_attrs_list: list = list(job_additional_info_attrs.keys())

Company = namedtuple('Company', company_attrs_list)
JobBasicInfo = namedtuple('JobBasicInfo', job_basic_info_attrs_list)
JobAdditionalInfo = namedtuple('JobAdditionalInfo', job_additional_info_attrs_list)


