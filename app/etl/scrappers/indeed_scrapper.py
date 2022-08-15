"""Python script to scrape Indeed.com for jobs.

Indeed.com is a job board that allows users to search for jobs based on
a given location and job title.

This script automate the process of scraping Indeed.com
for jobs from all the countries supported by Indeed.com (indeed.com/worldwide)
and saving the results in a CSV file(temporary).
"""
from collections import defaultdict, namedtuple
import json
from typing import Generator, Optional, Iterator, List
import bs4
from bs4 import BeautifulSoup
from loguru import logger

from utilities import decorators
from etl.utils.utils import Utils
from etl.utils.etls_common import CountriesScrapper, JobsCountriesScrapper, PagesNoScrapper  
from etl.utils.job_specifications import OrSpecification, JobDescriptionFilter
from models.job_models import JobBasicInfo, CompanyBasicInfo, JobCompanyBasicInfo, JobFullInfo, JobMoreInfo, Country
from etl.transformers.indeed_transformer import IndeedPagesNoTransformer, IndeedBasicJobCompanyInfoTransformer,IndeedMoreJobInfoTransformer, IndeedTransformerUtils,IndeedCountriesTransformer
from etl.apis.job_skills_api import JobSkillsAPI

class IndeedScrapper(CountriesScrapper,PagesNoScrapper,JobsCountriesScrapper):
    """Scrapper for Indeed Jobs"""

    def __init__(self, configs: dict, job_skills: str):
        "Initialize the Indeed Scrapper by loading the configs"
        print(json.dumps(configs,indent=4))
        self.countries_base_url = configs['countries_base_url']
        self.jobs_base_url = configs['jobs_base_url']
        self.job_base_url = configs['job_base_url']
        self.company_base_url = configs['company_base_url']
        self.job_skills = job_skills

    @decorators.timer
    def get_countries(self, countries_no: Optional[int] = None, countries_url: str = None) -> Iterator[Country]:
        """Get the list of countries supported by indeed"""
        if countries_url is None:
            countries_url = self.countries_base_url
        countries_soup: BeautifulSoup = Utils.get_page_parsed(countries_url)
        worldwide_countries: bs4.element.ResultSet = countries_soup.find("ul", class_="worldwide__countries")
        countries = worldwide_countries.find_all("a")
        countries_number = len(countries) if not countries_no else countries_no
        for pos in range(countries_number):
            country_name = countries[pos]
            country_link = country_name.get("href")
            country: Country = IndeedCountriesTransformer.transform(country_name,country_link)
            yield country

    @decorators.timer
    def get_pages_no(self, country_jobs_url: str) -> int:
        """Get the number of pages"""
        country_jobs_url_paged = country_jobs_url + '&start=' + "1000000"
        while True:
            try:
                results = IndeedScrapper.get_results_job_cards_collection(country_jobs_url_paged)
                pages_no_raw: bs4.element.Tag = results.find("div", id="searchCountPages")
                print("Pages No Raw",pages_no_raw)
                pages_no = IndeedPagesNoTransformer.transform(pages_no_raw)
                if pages_no:
                    break
            except AttributeError as attribute_error:
                logger.warning(f"AttributeError: {attribute_error}")
                continue
        return pages_no

    @decorators.timer
    def get_jobs_countries(
        self,
        countries_input: Generator[Country,None,None],
        job_title_input: str,
        page_no: Optional[int] = None,
    ) -> Generator[tuple[str,int,str],None,None]:
        """Get the list of jobs"""
        job_title = job_title_input.replace(" ", "+")
        for country in countries_input:
            country_name, country_code = country.country_name, country.country_code
            job_country: dict = {"country_code":country_code,"job_title":job_title}
            country_jobs_url = self.jobs_base_url % job_country
            max_page_no = page_no if page_no else self.get_pages_no(country_jobs_url)
            yield country_jobs_url, max_page_no, country_name

    def get_jobs_for_each_page(self, country_jobs_url: str, max_page_no: int) -> Generator[bs4.element.ResultSet,None,None]:
        """Get jobs for each country supported by indeed jobs website"""
        for page_no in range(max_page_no):
            jobs_url_paged = country_jobs_url + '&start=' + str(page_no)
            while True:
                try:
                    results = IndeedScrapper.get_results_job_cards_collection(jobs_url_paged)
                    jobs_raw_page: bs4.element.ResultSet = results.find_all("div", class_="cardOutline")
                    break
                except AttributeError as attribute_error:
                    logger.warning(f"AttributeError: {attribute_error}")
                    continue
            yield jobs_raw_page

    def get_basic_job_info(
        self, jobs_raw_page: bs4.element.ResultSet, country_name: str
    ) -> Generator[tuple[JobBasicInfo,CompanyBasicInfo],None,None]:
        """Get jobs per page (usually 15 jobs per page in indeed)"""
        for job in jobs_raw_page:
            job_title = job.find("h2", class_="jobTitle").find("a").find("span")
            job_id = job.find("h2", class_="jobTitle").find("a").get("id").split('job_')[-1]
            job_salary = job.find("div", class_="salaryOnly")
            company_name = job.find("span", class_="companyName")
            company_location = job.find("div", class_="companyLocation")
            company_rating = job.find("span", class_="ratingNumber")
            job_basic_info: JobBasicInfo = JobBasicInfo(job_title=job_title,job_id=job_id,job_salary=job_salary,job_url="")
            company_basic_info: CompanyBasicInfo = CompanyBasicInfo(company_name=company_name,company_location=company_location,company_rating=company_rating,company_country_name=country_name,company_url="")
            job_basic_info, company_basic_info = IndeedBasicJobCompanyInfoTransformer.transform(job_basic_info,company_basic_info,job_base_url = self.job_base_url,company_base_url = self.company_base_url)
            yield job_basic_info, company_basic_info
  
    @decorators.debug
    def get_more_job_info(
        self, job_basic_info: JobBasicInfo, company_basic_info: CompanyBasicInfo
    ) -> JobFullInfo:
        """Get the more job info when user clicks on the job card"""
        job_info_soup = Utils.get_page_parsed(job_basic_info.job_url)
        root_info = job_info_soup.find("div", id="viewJobSSRRoot")
        job_description = root_info.find("div", id="jobDescriptionText")
        job_benefits = root_info.find("div", id="benefits")
        posted_date = root_info.find("div", id="hiringInsightsSectionRoot").find("p", class_="jobsearch-HiringInsights-entry--bullet")
        job_more_info: JobMoreInfo = JobMoreInfo(job_description=job_description,job_benefits=job_benefits,job_posted_date=posted_date,job_skills=self.job_skills)
        job_more_info: JobMoreInfo = IndeedMoreJobInfoTransformer.transform(job_more_info)
        job_full_info = JobFullInfo(job_basic_info=job_basic_info,company_basic_info=company_basic_info,job_more_info=job_more_info)
        return job_full_info

    @staticmethod
    def get_results_job_cards_collection(jobs_url) -> bs4.element.Tag:
        """Get the results column which contain basic job cards info"""
        jobs_soup: BeautifulSoup = Utils.get_page_parsed(jobs_url)
        results = jobs_soup.find("td", id="resultsCol")
        return results


    @staticmethod
    def get_customized_indeed_country(country_name: str, country_code: str) -> Iterator[Country]:
        """Get the customized indeed country Iterator"""
        result = (Country(country_name=country_name, country_code=country_code) for _ in range(1))
        return result

