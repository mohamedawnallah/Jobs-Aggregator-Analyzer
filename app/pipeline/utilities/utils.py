"""Helpers module needed through out the application

Reusable functions that are used throughout the application from different modules
"""
import concurrent.futures
from typing import AsyncGenerator, Callable
import re
from aiostream import stream
from typing import Iterable, Union, Generator, Iterator, List
import yaml
import json
import bs4
import pandas as pd
import time
import aiohttp
import random
import asyncio
from bs4 import BeautifulSoup
from typing import Optional
from pipeline.utilities.helpers import DataFileReaderSingleton
from loguru import logger
from dotenv import load_dotenv

class Utils:
    """Utils Class"""
    @staticmethod
    def get_text(value: Union[bs4.element.Tag, str]) -> str:
        """Handling Null values in indeed jobs"""
        if not value:
            return None
        is_bs4_tag = isinstance(value, bs4.element.Tag)
        return value.text if is_bs4_tag else value
    
    @staticmethod
    def get_normalized_text(text: str) -> str:
        """Handling text format"""
        normalized_text = Utils.normalize_text(text)
        decoded_text = Utils.decode_text(normalized_text)
        return decoded_text

    @staticmethod
    def normalize_text(text: str) -> str:
        """Handling text format"""
        text = text.lower().strip()
        text = re.sub(r'\n', ' ', text)
        text = re.sub(' +', ' ', text)
        return text
    
    @staticmethod
    def decode_text(text: str) -> str:
        """Handling text format"""
        encoded_text = text.encode('utf-8')
        decoded_text = encoded_text.decode('utf-8')
        return decoded_text

    @staticmethod
    def get_digits_from_string(text: str) -> list[int]:
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
        text = Utils.get_normalized_text(text)
        search_words: str = "|".join(search_words)
        search_pattern = r"\b" + fr"({search_words})" + r"\b"
        all_words_found: List[str] = re.findall(search_pattern, text)
        all_words_found: str = ', '.join(all_words_found)
        return all_words_found

    @staticmethod
    def is_word_found(search_word: str, text: str) -> bool:
        """Check if the word is found in the given text"""
        search_word = Utils.get_normalized_text(search_word)
        search_pattern = r"\b" + re.escape(search_word) + r"\b"
        if not re.search(search_pattern, text):
            return False
        return True
    
    @staticmethod
    def find_bs4_element(soup: BeautifulSoup, element_name: str, attrs: Optional[dict[str,str]] = None) -> Optional[bs4.element.Tag]:
        """Find the bs4 element with the given name and class"""
        try:
            element: Optional[bs4.element.Tag] = soup.find(name=element_name, attrs=attrs)
        except AttributeError:
            element = None
        return element
    
    @staticmethod
    def find_bs4_elements(soup: BeautifulSoup, element_name: str, attrs: Optional[dict[str,str]] = None) -> Optional[bs4.element.ResultSet]:
        """Find the bs4 elements with the given name and class"""
        try:
            elements: Optional[bs4.element.ResultSet] = soup.find_all(name=element_name, attrs=attrs)
        except AttributeError:
            elements = None
        return elements
    
    @staticmethod
    def get_attribute_value_from_tag(element_tag: bs4.element.Tag, tag_name: str, attribute_name: str):
        try:
            attribute_element_value = element_tag.find(tag_name).get(attribute_name)
        except AttributeError:
            attribute_element_value = None
        return attribute_element_value
        
    @staticmethod
    async def get_page_parsed(url: str) -> BeautifulSoup:
        """Get the parsed page of the given html"""
        html: str = await Utils.request_proxy_url(url)
        soup: BeautifulSoup = Utils.get_beautiful_soup(html)
        return soup

    @staticmethod
    async def request_proxy_url(url: str, http_method: Optional[str] = 'GET', params: Optional[dict] = None, data: Optional[dict] = None, content_type: Optional[str] = 'application/text') -> BeautifulSoup:
        """Get the html for the given link"""
        proxy_api_endpoints: str = DataFileReaderSingleton.get_data(file_path="app/etl/settings/api_keys.txt")
        proxy_api_endpoint: str = random.choice(proxy_api_endpoints)
        proxy_api_url = proxy_api_endpoint % {'url':url}
        response: str = await Utils.request_url(url=proxy_api_url, http_method=http_method, params=params, data=data, content_type=content_type)
        return response

    @staticmethod
    async def request_url(url: str, http_method: Optional[str] = 'GET', params: Optional[dict] = None, data: Optional[dict] = None, content_type: Optional[str] = 'application/text') -> object:
        """Get the html for the given link"""
        headers = {'User-Agent':'Mozilla/5.0','Content-Type':content_type}
        while True:
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1500000),headers=headers) as session:
                    async with session.request(method=http_method, url=url, json=data, params=params) as response:
                        html = await response.text()
                        if response.status != 200:
                            logger.warning(f"Response Status is: {response.status} for url: {url}")
                            response.close()
                            await session.close()
                            continue
                        logger.info(f"Response Status is: {response.status} for url: {url}")
                        html = await response.text()
                return html
            except aiohttp.ClientError as client_error:
                logger.error(f"Client Error: {client_error}, {url}")
        
    @staticmethod
    def get_beautiful_soup(html: str) -> BeautifulSoup:
        """Get beautiful soup object"""
        return BeautifulSoup(html, "html.parser")

    @staticmethod
    def get_configs(configs_path: str = "app/pipeline/settings/pipeline_configs.yaml") -> dict:
        """Get the configs from the config file"""
        with open(configs_path, "r",encoding='utf-8') as configs_file:
            try:
                configs: dict = yaml.safe_load(configs_file)
            except yaml.YAMLError as yaml_error:
                logger.error(f"Error in loading yaml file: {yaml_error}")
        return configs

    @staticmethod
    def load_env_file(env_file_path: str) -> bool:
        is_env_file_loaded = load_dotenv(dotenv_path=env_file_path)
        return is_env_file_loaded

    @staticmethod
    def chunker(seq, size) -> Generator[Iterable,None,None]:
        """Chunk iterable to small multiple yielded pieces based on given size"""
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))
    
    @staticmethod
    #Chunk generator to small multiple yielded pieces based on given size
    def generator_chunker(seq, size) -> Generator[Iterable,None,None]:
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))
    
    @staticmethod
    async def get_stream_data_from_data_async_generators(data_async_generators: List[AsyncGenerator]) -> AsyncGenerator[object, None]:
        """Get the streaming data from the async generators"""
        data_async_generator = stream.merge(*data_async_generators)
        data_async_generator_stream = data_async_generator.stream()
        async with data_async_generator_stream as generator_data_stream:
            async for data in generator_data_stream:
                yield data
                
    @staticmethod
    def get_proxy_api_keys() -> List[str]:
        """Get the scrapper api keys from the file"""
        with open("app/etl/settings/api_keys.txt", "r") as api_keys_file:
            api_keys = api_keys_file.read().splitlines()
        return api_keys
  
