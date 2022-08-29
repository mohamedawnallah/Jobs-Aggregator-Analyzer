"""Python script to scrape Indeed.com for jobs.

Indeed.com is a job board that allows users to search for jobs based on
a given location and job title.

This script automate the process of scraping Indeed.com
for jobs from all the countries supported by Indeed.com (indeed.com/worldwide)
and saving the results in a CSV file(temporary).
"""
from typing import Generator, Optional, Iterator
import bs4
from bs4 import BeautifulSoup
from etl.utilities.utils import Utils
from etl.common.scrappers_common import CountriesScrapper, JobsCountriesScrapper, PagesNoScrapper  
from etl.models.job_models import JobBasicInfo, JobCompanyBasicInfo, JobFullInfo, JobMoreInfo, JobCountry
from etl.models.company_models import CompanyBasicInfo, CompanyMoreBasicInfo
from etl.models.country_model import Country
from transformers.scrappers.indeed_transformer import IndeedBasicJobInfoTransformer, IndeedCompanyBasicInfoTransformer, IndeedCompanyMoreBasicInfoTransformer, IndeedMoreJobInfoTransformer, IndeedCountriesTransformer
from loguru import logger

class IndeedScrapper(CountriesScrapper,PagesNoScrapper,JobsCountriesScrapper):
    """Scrapper for Indeed Jobs"""

    def __init__(self, configs: dict):
        "Initialize the Indeed Scrapper by loading the configs"
        print(configs)
        self.indeed_configs = configs['data_sources']['indeed']
        self.countries_base_url = self.indeed_configs['countries_base_url']
        self.jobs_base_url = self.indeed_configs['jobs_base_url']
        self.job_base_url = self.indeed_configs['job_base_url']
        self.company_base_url = self.indeed_configs['company_base_url']
        
    async def get_countries(self, countries_no: Optional[int] = None, countries_url: str = None) -> Generator[Country,None,None]:
        """Get the list of countries supported by indeed"""
        if countries_url is None:
            countries_url = self.countries_base_url
        countries_soup: BeautifulSoup =  await Utils.get_page_parsed(countries_url)
        worldwide_countries: bs4.element.ResultSet = countries_soup.find("ul", class_="worldwide__countries")
        countries = worldwide_countries.find_all("a")
        countries_number = len(countries) if not countries_no else countries_no
        for pos in range(countries_number):
            country_name = countries[pos]
            country_link = country_name.get("href")
            country: Country = IndeedCountriesTransformer.transform(country_name,country_link)
            yield country

    def is_last_page(self, jobs_page: bs4.element.Tag) -> int:
        """Get the number of pages"""
        is_last_page = False     
        if jobs_page.find("p",class_="dupetext"):
            is_last_page = True
            return is_last_page
        return is_last_page

    async def get_jobs_countries(self, countries_input: Generator[Country,None,None], job_title_input: str) -> Generator[JobCountry,None,None]:
        """Get the list of jobs"""
        job_title = job_title_input.replace(" ", "+")
        async for country in countries_input:
            country_name, country_code = country.country_name, country.country_code
            country_jobs_url = self.jobs_base_url % {"country_code":country_code,"job_title":job_title}
            job_country: JobCountry = JobCountry(country_name=country_name,country_jobs_url=country_jobs_url)
            yield job_country

    async def get_jobs_for_each_page(self, country_jobs_url: str, page_no_input: Optional[int] = None) -> Generator[bs4.element.ResultSet,None,None]:
        """Get jobs for each country supported by indeed jobs website"""
        if not page_no_input and page_no_input == 0:
            return
        page_no = 0
        should_exit = False
        while not should_exit:
            while True:
                jobs_url_paged = country_jobs_url + '&start=' + str(page_no)
                try:
                    results =  await IndeedScrapper.get_results_job_cards_collection(jobs_url_paged)
                    jobs_raw_page: bs4.element.ResultSet = results.find_all("div", class_="cardOutline")
                    break
                except AttributeError as attribute_error:
                    logger.warning(f"AttributeError: {attribute_error}")
                    continue
            yield jobs_raw_page
            if self.is_last_page(results):
                should_exit = True
                break
            page_no += 10
            should_exit = page_no_input <= (page_no // 10) if page_no_input else False
            print("Page No is: ", page_no, "and Url is: ", country_jobs_url)

    def get_job_basic_info(
        self, jobs_raw_page: bs4.element.ResultSet
    ) -> Generator[JobBasicInfo,None,None]:
        """Get jobs per page (usually 15 jobs per page in indeed)"""
        for job in jobs_raw_page:
            job_title = job.find("h2", class_="jobTitle").find("a").find("span")
            job_id = job.find("h2", class_="jobTitle").find("a").get("id").split('job_')[-1]
            job_salary = job.find("div", class_="salaryOnly")
            job_basic_info: JobBasicInfo = JobBasicInfo(job_title=job_title,job_id=job_id,job_salary=job_salary,job_url=self.job_base_url)
            job_basic_info: JobBasicInfo = IndeedBasicJobInfoTransformer.transform(job_basic_info)
            yield job_basic_info
    

    def get_cmp_basic_info(self, jobs_raw_page: bs4.element.ResultSet, country_name) -> CompanyBasicInfo:
        """Get the company info"""
        for job in jobs_raw_page:
            company_name = job.find("span", class_="companyName")
            company_location = job.find("div", class_="companyLocation")
            company_rating = job.find("span", class_="ratingNumber")
            company_basic_info: CompanyBasicInfo = CompanyBasicInfo(company_name=company_name, company_rating=company_rating, company_location=company_location, company_jobs_platform_url=self.company_base_url, company_country_name=country_name)
            company_basic_info: CompanyBasicInfo = IndeedCompanyBasicInfoTransformer.transform(company_basic_info)
            yield company_basic_info

    async def get_cmp_more_basic_info(self, company_jobs_platform_url: str):
        """Get Company More Basic Info"""
        company_more_basic_info_soup = await Utils.get_page_parsed(company_jobs_platform_url)
        try:
            company_founded_year: bs4.element.Tag = company_more_basic_info_soup.find("li",{"data-testid":"companyInfo-founded"},recursive=True)
        except AttributeError:
            company_founded_year = None
        try:
            company_employees_size: bs4.element.Tag = company_more_basic_info_soup.find("li",{"data-testid":"companyInfo-employee"},recursive=True)
        except AttributeError:
            company_employees_size = None
        try:
            company_revenue: bs4.element.Tag = company_more_basic_info_soup.find("li",{"data-testid":"companyInfo-revenue"},recursive=True)
        except AttributeError:
            company_revenue = None
        try:
            company_industry: bs4.element.Tag = company_more_basic_info_soup.find("li",{"data-testid":"companyInfo-industry"},recursive=True)
        except AttributeError:
            company_industry = None
        try:
            company_website: bs4.element.Tag = company_more_basic_info_soup.find("li",{"data-testid":"companyInfo-companyWebsite"},recursive=True).find("a",recursive=True).get("href")
        except AttributeError:
            company_website = None

        company_more_basic_info: CompanyBasicInfo = CompanyMoreBasicInfo(company_founded_year=company_founded_year,company_employees_size=company_employees_size,company_revenue=company_revenue,company_industry=company_industry,company_website=company_website)
        company_more_basic_info: CompanyMoreBasicInfo = IndeedCompanyMoreBasicInfoTransformer.transform(company_more_basic_info)

        return company_more_basic_info
    
    async def get_job_more_info(
        self, job_company_basic_info: JobCompanyBasicInfo 
    ) -> JobFullInfo:
        """Get the more job info when user clicks on the job card"""
        job_basic_info: JobBasicInfo = job_company_basic_info.job_basic_info
        company_basic_info: CompanyBasicInfo = job_company_basic_info.company_basic_info
        company_more_basic_info: CompanyMoreBasicInfo = job_company_basic_info.company_more_basic_info
        job_info_soup =  await Utils.get_page_parsed(job_basic_info.job_url)
        root_info = job_info_soup.find("div", id="viewJobSSRRoot")
        try:
            job_description = root_info.find("div", id="jobDescriptionText")
        except AttributeError :
            job_description = None
        try:
            job_benefits = root_info.find("div", id="benefits")
        except AttributeError:
            job_benefits = None
        try:
            posted_date = root_info.find("div", id="hiringInsightsSectionRoot").find("p", class_="jobsearch-HiringInsights-entry--bullet")
        except AttributeError:
            posted_date = None
        job_more_info: JobMoreInfo = JobMoreInfo(job_description=job_description,job_benefits=job_benefits,job_posted_date=posted_date)
        job_more_info: JobMoreInfo = IndeedMoreJobInfoTransformer.transform(job_more_info)
        job_full_info = JobFullInfo(job_basic_info=job_basic_info,company_basic_info=company_basic_info,company_more_basic_info=company_more_basic_info,job_more_info=job_more_info)
        return job_full_info

    @staticmethod
    async def get_results_job_cards_collection(jobs_url) -> bs4.element.Tag:
        """Get the results column which contain basic job cards info"""
        jobs_soup: BeautifulSoup =  await Utils.get_page_parsed(jobs_url)
        results = jobs_soup.find("td", id="resultsCol")
        return results

    @staticmethod
    def get_customized_indeed_country(country_names: str, country_codes: str) -> Iterator[Country]:
        """Get the customized indeed country Iterator"""
        for country_name, country_code in zip(country_names,country_codes):
            yield Country(country_name=country_name,country_code=country_code)

    
    @staticmethod
    async def get_indeed_job_items(job_country: JobCountry, indeed_scrapper: "IndeedScrapper", pages_no: int) -> Generator[dict,None,None]:
        """Indeed Full Info Job Items"""
        country_name, country_jobs_url = job_country.country_name, job_country.country_jobs_url
        jobs_raw_pages: Generator[bs4.element.ResultSet,None,None] = indeed_scrapper.get_jobs_for_each_page(country_jobs_url,pages_no)
        async for full_job_info in IndeedScrapper._get_full_jobs_infos(jobs_raw_pages, indeed_scrapper, country_name):
            yield full_job_info
            

    @staticmethod
    async def _get_full_jobs_infos(jobs_raw_pages, indeed_scrapper: "IndeedScrapper", country_name):
        async for jobs_raw_page in jobs_raw_pages:
            job_basic_infos: Generator[JobBasicInfo,None,None] = indeed_scrapper.get_job_basic_info(jobs_raw_page)
            company_basic_infos: Generator[CompanyBasicInfo,None,None] = indeed_scrapper.get_cmp_basic_info(jobs_raw_page,country_name)
            async for job_basic_info in IndeedScrapper._get_full_job_info(job_basic_infos, company_basic_infos, indeed_scrapper):
                yield job_basic_info
        
    @staticmethod            
    async def _get_full_job_info(job_basic_infos: Generator[JobBasicInfo,None,None], company_basic_infos: Generator[CompanyBasicInfo,None,None], indeed_scrapper: "IndeedScrapper"):
        for job_basic_info, company_basic_info in zip(job_basic_infos,company_basic_infos):
            company_more_basic_info: CompanyMoreBasicInfo = await indeed_scrapper.get_cmp_more_basic_info(company_basic_info.company_jobs_platform_url)
            job_company_basic_info: JobCompanyBasicInfo = JobCompanyBasicInfo(job_basic_info=job_basic_info,company_basic_info=company_basic_info,company_more_basic_info=company_more_basic_info)
            job_full_info: JobFullInfo = await indeed_scrapper.get_job_more_info(job_company_basic_info)
            job_full_info: dict = job_full_info.to_dict()
            yield job_full_info

