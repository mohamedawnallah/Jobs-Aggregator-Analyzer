"""Helpers module needed through out the application

Reusable functions that are used throughout the application from different modules
"""
from abc import ABC, abstractmethod
from collections import namedtuple
from collections import defaultdict
from typing import Optional, Union
import re
import toml
import bs4
from bs4 import BeautifulSoup
import requests
class Scrapper(ABC):
    """Scrapper Abstract Class for other Web Scrappers"""
    @abstractmethod
    def get_countries(self, end_pos: Optional[int] = None) -> dict:
        """Get the list of countries supported by indedd"""
        pass
    
    @abstractmethod
    def get_jobs_countries(self, countries_input: dict, job_title_input: str,
                             page_no: Optional[int] = None):
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


    @staticmethod
    def get_configs(configs_path) -> dict:
        """Get the configs from the config file"""
        configs = toml.load(configs_path)
        return configs


    @staticmethod
    def get_csv_header(main_configs : dict, skills_name_config: str) -> list[str]:
        """Get csv header"""
        if not isinstance(skills_name_config, str):
            raise CSVHeaderError("Skill name config must be a string refers to\
                                  the corresponding one in the config file (skills section)")

        Company: namedtuple = Utils.get_cls_named_tuple(configs=main_configs, configs_key='company',
                                                        cls_name='Company')
        JobBasicInfo: namedtuple = Utils.get_cls_named_tuple(configs=main_configs, configs_key='job_basic_info',
                                                             cls_name='JobBasicInfo')
        JobAdditionalBasicInfo:  namedtuple = Utils.get_cls_named_tuple(configs=main_configs, configs_key='job_additional_basic_info',
                                                                        cls_name='JobAdditionalBasicInfo')
        JobSkills: namedtuple = Utils.get_cls_named_tuple(configs=main_configs, configs_key=skills_name_config,
                                                          cls_name='JobSkills')
        company_keys = list(Company._fields)
        job_basic_info_keys = list(JobBasicInfo._fields)
        job_additional_basic_info_keys = list(JobAdditionalBasicInfo._fields)
        job_skills_keys = list(JobSkills._fields)

        csv_header = job_basic_info_keys + job_additional_basic_info_keys\
                     + company_keys + job_skills_keys
        return csv_header


    @staticmethod
    def get_cls_named_tuple(configs: dict,configs_key: str, cls_name: str) -> namedtuple:
        """Get Class named tuple named tuple"""
        if not isinstance(configs, dict):
            raise InvalidConfigError("Configs must be a dictionary")

        if not isinstance(configs_key, str):
            raise TypeError("Configs Key must be a string")
        
        if not isinstance(cls_name, str):
            raise TypeError("Class Name must be a string for the named tuple")

        key_configs = dict()
        is_job_configs = configs_key.strip().startswith('job') and configs_key.strip().endswith('info')

        if not is_job_configs:
            key_configs: dict = Utils.get_value_key_attr(configs,configs_key)
        
        if is_job_configs:
            job_configs: dict = Utils.get_value_key_attr(configs,'job')
            key_configs = Utils.get_value_key_attr(job_configs,configs_key)

        keys: list = list(key_configs.keys())
        return namedtuple(cls_name, keys)    


    @staticmethod
    def get_value_key_attr(configs_input: dict,key:str) -> dict:
        """Get values of key given key attribute from config file regards to 
        the job info, company info, data engineering skills and more"""
        try:
            if key in configs_input: return configs_input[key]
            for k,v in configs_input.items():
                if isinstance(v,dict):
                    return Utils.get_value_key_attr(v,key)
        except KeyError as key_error:
            raise KeyError(f"Key {key} not found in config file",key_error)

class InvalidUrlError(Exception):
    """Invalid Url Custom Exception"""
    pass


class CSVHeaderError(Exception):
    """CSV Header Custom Exception"""
    pass    

class InvalidConfigError(Exception):
    """Invalid Config Custom Exception"""
    pass


if __name__ == '__main__':
    pass
