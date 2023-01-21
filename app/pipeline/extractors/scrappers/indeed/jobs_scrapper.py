

from typing import Generator, Optional, Iterator
import bs4
from bs4 import BeautifulSoup
from typing import List, AsyncGenerator
import pandas as pd
from aiostream import stream
from pipeline.utilities.utils import Utils
from common.etls_common import ExtractorAsync
from pipeline.common.scrappers_common import JobsScrapper, PagesNoScrapper  
from models.job_model import JobBasicInfo, JobMoreInfo, JobDim
from pipeline.transformers.scrappers.indeed.jobs_transformer import IndeedJobBasicInfoTransformer, IndeedJobMoreInfoTransformer
from models.country_model import CountryDim

import json
from loguru import logger

class IndeedJobsScrapper(ExtractorAsync, PagesNoScrapper,JobsScrapper):
    """Scrapper for Indeed Jobs"""
    def __init__(self, indeed_configs: dict):
        "Initialize the Indeed Scrapper by loading the configs"
        self.jobs_base_url = indeed_configs['jobs_base_url']
        self.job_base_url = indeed_configs['job_base_url']
        self.company_base_url = indeed_configs['company_base_url']
    
    async def extract(self, countries: Generator[CountryDim, None, None], job_title: str, pages_no: Optional[int] = None) -> pd.DataFrame:
        """Extract the Indeed Jobs HTML"""
        job_dim_countries_generator: List[AsyncGenerator[JobDim,None]] =  await self.get_jobs_in_countries(countries, job_title, pages_no)
        jobs_df = await self.get_jobs_in_countries_df(job_dim_countries_generator)
        return jobs_df

    async def get_jobs_in_countries(self, countries: Generator[CountryDim, None, None], job_title: str, pages_no: Optional[int] = None) -> List[AsyncGenerator[JobDim,None]]:
        jobs_dim_countries_generator = [self.get_jobs_in_country(country, job_title, pages_no)  for country in countries]            
        return jobs_dim_countries_generator
    
    async def get_jobs_in_country(self, country: CountryDim, job_title: str, pages_no: Optional[int] = None) -> AsyncGenerator[JobDim,None]:
        """Indeed Full Info Job Items"""
        country_jobs_url = self.jobs_base_url % {"country_code":country.country_code,"job_title":job_title}
        job_dim_generator: AsyncGenerator[JobDim,None] = self.get_job_dim_generator(country_jobs_url, country.country_name, pages_no)
        async for job_dim in job_dim_generator:
            yield job_dim   

    async def get_jobs_in_countries_df(self, job_dim_generators: List[AsyncGenerator[JobDim,None]]) -> pd.DataFrame:
        """Saving Streams to staging csv"""
        job_dim_generator: AsyncGenerator[JobDim, None] = Utils.get_stream_data_from_data_async_generators(job_dim_generators)
        jobs_in_countries_df: pd.DataFrame = await self.get_jobs_df(job_dim_generator)
        return jobs_in_countries_df
    
    async def get_jobs_in_country_df(self, job_dim_generator: AsyncGenerator[JobDim, None]) -> pd.DataFrame:
        """Saving Streams to staging csv"""
        jobs_in_countries_df: pd.DataFrame = await self.get_jobs_df(job_dim_generator)
        return jobs_in_countries_df

    async def get_jobs_df(self, job_dim_generator: AsyncGenerator[JobDim,None]) -> pd.DataFrame:
        jobs_df: Optional[pd.DataFrame] = None
        indx = 1
        async for job_dim in job_dim_generator:
            print(json.dumps(job_dim.to_dict(),indent=4))
            if indx == 1:
                jobs_df = pd.DataFrame(job_dim.to_dict(),index=[indx])
            else:
                new_jobs_df = pd.DataFrame(job_dim.to_dict(),index=[indx])
                jobs_df = pd.concat([jobs_df, new_jobs_df],axis=0)
            indx += 1
        return jobs_df
    
    async def get_job_dim_generator(self, country_jobs_url: str, country_name: str, pages_no: str) -> AsyncGenerator[JobDim,None]:
        """Get the more job info when user clicks on the job card"""
        # run the job cards in parallel
        async for jobs_per_page in self.get_jobs_for_each_page_generator(country_jobs_url,pages_no):
            # run the job cards in parallel
            jobs_basic_infos: List[JobBasicInfo] = [self.get_job_basic_info(job, country_name) for job in jobs_per_page]
            job_dim_generators: List[AsyncGenerator[JobDim, None]] = [self.get_job_dim(job_basic_info, country_name) for job_basic_info in jobs_basic_infos]
            job_dim_generator = Utils.get_stream_data_from_data_async_generators(job_dim_generators)
            async for job_dim in job_dim_generator:
                yield job_dim
    
    async def get_jobs_for_each_page_generator(self, country_jobs_url: str, page_no_input: Optional[int] = None) -> AsyncGenerator[bs4.element.ResultSet, None]:
        """Get jobs for each country supported by indeed jobs website"""
        if page_no_input and page_no_input == 0:
            return
        page_no = 0
        should_exit = False
        while not should_exit:
            jobs_page_url = country_jobs_url + '&start=' + str(page_no)
            jobs_soup: BeautifulSoup =  await Utils.get_page_parsed(jobs_page_url)
            job_cards_per_page_raw = await self.jobs_per_page(jobs_soup)
            yield job_cards_per_page_raw
            is_last_page = self.is_last_page(jobs_soup)
            if is_last_page:
                break
            page_no += 10
            should_exit = page_no_input <= (page_no // 10) if page_no_input else False

    async def jobs_per_page(self, jobs_soup: bs4.element.Tag) -> bs4.element.ResultSet:
        """Get the results column which contain basic job cards info"""
        jobs: Optional[bs4.element.ResultSet] = Utils.find_bs4_elements(jobs_soup, "div", {"class":"cardOutline"})
        return jobs

    def get_job_basic_info(self, job: bs4.element.Tag, country_name: str) -> List[JobBasicInfo]:
        """Get jobs per page (usually 15 jobs per page in indeed)"""
        job_title: Optional[bs4.element.Tag] = Utils.find_bs4_element(job, "h2", {"class":"jobTitle"})
        job_link: Optional[bs4.element.Tag] =  Utils.find_bs4_element(job_title, "a")
        job_link: Optional[bs4.element.Tag] = Utils.find_bs4_element(job_link, "span")
        job_platform_id: Optional[str] = Utils.get_attribute_value_from_tag(job_title, 'a', 'id').split('_')[-1]
        job_posted_date: Optional[bs4.element.Tag] = Utils.find_bs4_element(job, "span", {"class":"date"})
        job_city: Optional[bs4.element.Tag] = Utils.find_bs4_element(job, "div", {"class":"companyLocation"})
        company_name: Optional[bs4.element.Tag] = Utils.find_bs4_element(job, "span",{"class": "companyName"})
        company_job_platform_url= Utils.get_attribute_value_from_tag(company_name, "a", "href")
        company_job_platform_url = company_job_platform_url if company_job_platform_url else company_name
        job_basic_info: JobBasicInfo = JobBasicInfo(title=job_title, platform_id=job_platform_id, url=self.job_base_url, posted_date=job_posted_date, company_name=company_name, company_job_platform_url=company_job_platform_url, city=job_city, is_remote=False, country=country_name)
        job_basic_info: JobBasicInfo = IndeedJobBasicInfoTransformer.transform(job_basic_info, self.company_base_url)
        return job_basic_info

    async def get_job_dim(self, job_basic_info: JobBasicInfo, country_name: int) -> JobDim:
        """Get the job dimension"""
        job_more_info: JobMoreInfo = await self.get_job_more_info(job_basic_info)
        job_dim: JobDim = JobDim(job_basic_info=job_basic_info, job_more_info=job_more_info)
        yield job_dim
    
    async def get_job_more_info(self, job_basic_info: JobBasicInfo) -> JobMoreInfo:
        """Get more job info when user clicks on the job card"""
        job_info_soup =  await Utils.get_page_parsed(job_basic_info.url)
        job_description: Optional[bs4.element.Tag] = Utils.find_bs4_element(job_info_soup, "div", {"id":"jobDescriptionText"})
        job_benefits: Optional[bs4.element.Tag] = Utils.find_bs4_element(job_info_soup, "div", {"id":"benefits"})
        job_more_info: JobMoreInfo = JobMoreInfo(description=job_description,benefits=job_benefits)
        job_more_info: JobMoreInfo = await IndeedJobMoreInfoTransformer.transform(job_more_info)
        return job_more_info
            
    def is_last_page(self, jobs_page: bs4.element.Tag) -> int:
        """Get the number of pages"""
        is_last_page_found: Optional[bs4.element.Tag] = Utils.find_bs4_element(jobs_page, "div", {"class":"show-omitted-jobs"})
        return True if is_last_page_found else False


