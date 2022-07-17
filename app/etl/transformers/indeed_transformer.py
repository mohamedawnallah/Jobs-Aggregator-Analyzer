from collections import namedtuple
import re
from loguru import logger
import bs4
from etl.utils.utils import Utils
from etl.models.job_dataclasses import Country, JobCompanyBasicInfo, JobBasicInfo, JobMoreInfo, CompanyBasicInfo, JobFullInfo
from etl.utils.etls_common import JobCompanyBasicInfoTransformer, JobMoreInfoTransformer, JobPagesNoTransformer, JobSkillsTransformer, CountriesTransformer
from etl.utils.job_specifications import JobDescriptionFilter, BaseSpecification

class IndeedBasicJobCompanyInfoTransformer(JobCompanyBasicInfoTransformer):
    """Indeed Basic Job Info Transformer"""
    @staticmethod
    def transform(job_basic_info: JobBasicInfo, company_basic_info: CompanyBasicInfo,**kwargs) -> tuple[JobBasicInfo,CompanyBasicInfo]:
        """Transform the basic job company info to a namedtuple"""
        job_base_url = kwargs['job_base_url']
        company_base_url = kwargs['company_base_url']
        job_title = Utils.get_valid_value(job_basic_info.job_title)
        job_id = Utils.get_valid_value(job_basic_info.job_id)
        job_salary = Utils.get_valid_value(job_basic_info.job_salary)
        company_name = Utils.get_valid_value(company_basic_info.company_name)
        company_location = Utils.get_valid_value(company_basic_info.company_location)
        company_rating = Utils.get_valid_value(company_basic_info.company_rating)
        country_name = Utils.get_valid_value(company_basic_info.country_name)
        job_id = IndeedTransformerUtils.get_valid_job_id(job_id)
        job_url = IndeedTransformerUtils.get_job_url(job_base_url, job_id)
        company_url = IndeedTransformerUtils.get_company_url(company_base_url, company_name)
        job_basic_info: namedtuple = JobBasicInfo(job_title=job_title,job_id=job_id,job_salary=job_salary,job_url=job_url)
        company_basic_info: namedtuple = CompanyBasicInfo(company_name=company_name,company_url=company_url,company_location=company_location,company_rating=company_rating,country_name=country_name)
        return job_basic_info, company_basic_info

class IndeedMoreJobInfoTransformer(JobMoreInfoTransformer):
    """Indeed More Job Info Transformer Abstract Class"""
    @staticmethod
    def transform(job_info: JobMoreInfo,**kwargs) -> JobMoreInfo:
        """Transform the more job info"""
        posted_date: str = Utils.get_valid_value(job_info.job_posted_date)
        job_description: str = Utils.get_valid_value(job_info.job_description)
        job_benefits: str = IndeedTransformerUtils.get_valid_job_benfits(job_info.job_benefits)
        job_more_info = JobMoreInfo(job_description,job_benefits,posted_date,)
        return job_more_info

class IndeedJobSkillsTransformer(JobSkillsTransformer):
    """Indeed Full Job Info Transformer Abstract Class"""
    @staticmethod
    def transform(job_specifications: BaseSpecification, job_description: str) -> dict[str]:
        """Transform Full Job Info"""
        
        job_skills: dict[str] = JobDescriptionFilter.filter(job_specifications, job_description)
        return job_skills

class IndeedPagesNoTransformer(JobPagesNoTransformer):
    """Indeed Pages Transformer Abstract Class"""
    @staticmethod
    def transform(pages_no_raw: bs4.element.Tag) -> dict:
        """Transform the job info"""
        pages_no = Utils.get_valid_value(pages_no_raw)
        pages_no: list[str] = Utils.get_numbers_from_string(pages_no)
        pages_no = min(pages_no) * 10
        return pages_no


class IndeedCountriesTransformer(CountriesTransformer):
    """Countries Transformer Abstract Class"""
    @staticmethod
    def transform(country_name: str, country_link: str) -> Country:
        """Transform the country name"""
        country_name = Utils.get_valid_value(country_name)
        country_link = Utils.get_valid_value(country_link)
        country_code = country_link.split("//")[1].split(".")[0]
        country: Country = Country(country_name, country_code)
        return country

class IndeedTransformerUtils:
    """Indeed Transformer Utils"""
    @staticmethod
    def get_valid_job_benfits(benefits_section) -> str:
        """Get the benefits"""
        result = (
            "N/A"
            if not benefits_section
            else benefits_section.find_all("div", class_="css-1f2yqp0 e1xnxm2i0")
        )
        all_benefits = ""
        if result != "N/A":
            all_benefits = IndeedTransformerUtils.transform_job_benefits(result)
        return all_benefits

    @staticmethod
    def transform_job_benefits(benefits_raw: str) -> str:
        """Getting jobs benefits mentioned in job indeed page"""
        benefits_str = ""
        for benefit in benefits_raw:
            benefit_value = Utils.get_valid_value(benefit)
            benefits_str += benefit_value + ", "
        return benefits_str

    @staticmethod
    def get_valid_job_id(job_id: str):
        """Get a valid job id"""
        valid_job_id = job_id.split("jk=")[-1].split("&")[0]
        return valid_job_id

    @staticmethod
    def get_job_url(job_base_url: str, job_id: str) -> str:
        """Get the job link from job id"""
        job_url = job_base_url % {"job_id": job_id}
        return job_url

    @staticmethod
    def get_company_url(company_base_url: str, company_name: str) -> str:
        """Get the company website from company name"""
        company_url = company_base_url % {"company_name": company_name}
        company_url = company_url.replace(" ", "%20")
        return company_url

