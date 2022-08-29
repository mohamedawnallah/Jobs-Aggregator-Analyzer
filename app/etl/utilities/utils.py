"""Helpers module needed through out the application

Reusable functions that are used throughout the application from different modules
"""
import concurrent.futures
import re
from typing import Iterable, Union, Generator, Iterator, List
import yaml
import bs4
import aiohttp
from bs4 import BeautifulSoup
from dotenv import load_dotenv

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
        text = re.sub(' +', ' ', text)
        text = text.replace(",", "")
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
                continue
        return True

    @staticmethod
    def get_all_found_words(search_words: List[str], text) -> str:
        """Get all the found words in the given text"""
        text = Utils.get_valid_text(text)
        search_words: str = "|".join(search_words)
        search_pattern = r"\b" + fr"({search_words})" + r"\b"

        all_words_found: List[str] = re.findall(search_pattern, text)
        all_words_found: str = ', '.join(all_words_found)
        return all_words_found
        # all_search_words_found = ""
        # search_words_list: List[str] = list(search_words)
        # search_words_chunker_count: int = 15
        # search_words_chunker_generator = Utils.chunker(search_words_list,search_words_chunker_count)
        # with concurrent.futures.ProcessPoolExecutor() as executor:
        #     search_words_results = []
        #     for search_words_chunked_list in search_words_chunker_generator:
        #         search_words_result = executor.submit(Utils._get_all_found_words_helper,search_words_chunked_list,text)
        #         search_words_results.append(search_words_result)
        #     for search_words_final_result in concurrent.futures.as_completed(search_words_results):
        #         search_words_found = search_words_final_result.result()
        #         if search_words_found:
        #             all_search_words_found += search_words_found 
        # return all_search_words_found


    @staticmethod
    def is_word_found(search_word: str, text: str) -> bool:
        """Check if the word is found in the given text"""
        search_word = Utils.get_valid_text(search_word)
        search_pattern = r"\b" + re.escape(search_word) + r"\b"
        if not re.search(search_pattern, text):
            return False
        return True
    
    @staticmethod
    async def get_page_parsed(url: str) -> BeautifulSoup:
        """Get the parsed page of the given html"""
        html: str = await Utils.get_html_page(url)
        soup: BeautifulSoup = Utils.get_beautiful_soup(html)
        return soup

    @staticmethod
    async def get_html_page(url: str) -> BeautifulSoup:
        """Get the html for the given link"""
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        while True:
            try:
                async with aiohttp.ClientSession(headers=headers) as session:
                    response = await session.request('GET',url)
                    html = await response.text()
                    return html
            except aiohttp.ClientConnectionError as connection_error:
                print(f"Connection Error: {connection_error}")
                continue
            except aiohttp.ClientError as missing_schema_error:
                print(f"Missing Schema Error: {missing_schema_error}")
                
    @staticmethod
    def get_beautiful_soup(html: str) -> BeautifulSoup:
        """Get beautiful soup object"""
        return BeautifulSoup(html, "html.parser")

    @staticmethod
    def get_configs(configs_path: str = "app/etl/settings/etl_configs.yaml") -> dict:
        """Get the configs from the config file"""
        with open(configs_path, "r",encoding='utf-8') as configs_file:
            try:
                configs: dict = yaml.safe_load(configs_file)
            except yaml.YAMLError as yaml_error:
                print(yaml_error)
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
    def load_env_file(env_file_path: str) -> bool:
        is_env_file_loaded = load_dotenv(dotenv_path=env_file_path)
        return is_env_file_loaded

    @staticmethod
    def chunker(seq, size) -> Generator[Iterable,None,None]:
        """Chunk iterable to small multiple yielded pieces based on given size"""
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))