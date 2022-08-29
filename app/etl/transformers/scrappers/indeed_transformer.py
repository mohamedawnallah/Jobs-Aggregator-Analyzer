from collections import namedtuple
from typing import List
import bs4
import pandas as pd
from etl.utilities.utils import Utils
from etl.models.job_models import JobBasicInfo, JobMoreInfo, CompanyBasicInfo
from etl.models.company_models import CompanyBasicInfo, CompanyMoreBasicInfo
from etl.models.country_model import Country
from etl.common.transformers_common import Transformer


global i
i = 0
class IndeedBasicJobInfoTransformer(Transformer):
    """Indeed Basic Job Info Transformer"""
    @staticmethod
    def transform(job_basic_info: JobBasicInfo) -> JobBasicInfo:
        """Transform the basic job company info to a namedtuple"""
        job_title = Utils.get_valid_value(job_basic_info.job_title)
        job_id = Utils.get_valid_value(job_basic_info.job_id)
        job_salary = Utils.get_valid_value(job_basic_info.job_salary)
        job_id = IndeedTransformerUtils.get_valid_job_id(job_id)
        job_url = IndeedTransformerUtils.get_job_url(job_basic_info.job_url, job_id)
        job_basic_info: namedtuple = JobBasicInfo(job_title=job_title,job_id=job_id,job_salary=job_salary,job_url=job_url)
        return job_basic_info

class IndeedCompanyBasicInfoTransformer(Transformer):
    """Indeed Basic Job Info Transformer"""
    @staticmethod
    def transform(company_basic_info: CompanyBasicInfo) -> CompanyBasicInfo:
        """Transform the basic job company info to a namedtuple"""
        company_name = Utils.get_valid_value(company_basic_info.company_name)
        company_location = Utils.get_valid_value(company_basic_info.company_location)
        company_rating = Utils.get_valid_value(company_basic_info.company_rating)
        company_country_name = Utils.get_valid_value(company_basic_info.company_country_name)
        company_jobs_platform_url = IndeedTransformerUtils.get_company_url(company_basic_info.company_jobs_platform_url, company_name)
        comany_basic_info: namedtuple = CompanyBasicInfo(company_name=company_name,company_rating=company_rating,company_jobs_platform_url=company_jobs_platform_url,company_location=company_location,company_country_name=company_country_name)
        return comany_basic_info

class IndeedCompanyMoreBasicInfoTransformer(Transformer):
    """Indeed Basic Job Info Transformer"""
    @staticmethod
    def transform(company_basic_info: CompanyMoreBasicInfo) -> CompanyBasicInfo:
        """Transform the basic job company info to a namedtuple"""
        company_founded_year = Utils.get_valid_value(company_basic_info.company_founded_year)
        company_employees_size = Utils.get_valid_value(company_basic_info.company_employees_size)
        company_revenue = Utils.get_valid_value(company_basic_info.company_revenue)
        company_industry = Utils.get_valid_value(company_basic_info.company_industry)
        company_website = Utils.get_valid_value(company_basic_info.company_website)
        company_more_basic_info: CompanyBasicInfo = CompanyMoreBasicInfo(company_founded_year=company_founded_year,company_employees_size=company_employees_size,company_revenue=company_revenue,company_industry=company_industry,company_website=company_website)
        return company_more_basic_info

class IndeedMoreJobInfoTransformer(Transformer):
    """Indeed More Job Info Transformer Abstract Class"""
    @staticmethod
    def transform(job_info: JobMoreInfo) -> JobMoreInfo:
        """Transform the more job info"""
        posted_date: str = Utils.get_valid_value(job_info.job_posted_date)
        job_description: str = Utils.get_valid_value(job_info.job_description)
        job_benefits: str = IndeedTransformerUtils.get_valid_job_benfits(job_info.job_benefits)
        job_more_info = JobMoreInfo(job_description=job_description,job_benefits=job_benefits,job_posted_date=posted_date)
        return job_more_info

class IndeedJobSkillsTransformer(Transformer):
    """Indeed Full Job Info Transformer Abstract Class"""
    @staticmethod
    def transform(job_skills: str) -> str:
        """Transform Full Job Info"""
        job_skills: str = job_skills.strip()
        return job_skills

    @staticmethod
    def get_job_skills(all_job_skills: List[str], job_description: str) -> str:
        """Extract Job Skills from job description"""
        job_skills_found: str = Utils.get_all_found_words(all_job_skills,job_description)
        global i
        i += 1
        print("Job Skills Found: ", job_skills_found, "In the Row: ", i)
        
        return job_skills_found

class IndeedCompanyTransformer(Transformer):
    """Indeed Company Transformer"""

    @staticmethod
    def transform(jobs_series_df: pd.Series, companies: List[dict]) -> str:
        """Transform Full Job Info"""
        for company in companies:
            if company['company_name_found'] == jobs_series_df['company_name']:
                jobs_series_df['company_city'] = company['company_city']
                jobs_series_df['company_state'] = company['company_state']
                jobs_series_df['company_postal_code'] = company['company_postal_code']
                jobs_series_df['company_naics'] = company['company_naics']
                jobs_series_df['company_original_website'] = company['company_original_website']
                jobs_series_df['is_company_staffing'] = company['is_company_staffing']
                jobs_series_df['is_company_fortune_1000'] = company['is_company_fortune_1000']
                break
        return jobs_series_df
        

class IndeedPagesNoTransformer(Transformer):
    """Indeed Pages Transformer Abstract Class"""
    @staticmethod
    def transform(pages_no_raw: bs4.element.Tag) -> dict:
        """Transform the job info"""
        pages_no: list[str] = Utils.get_numbers_from_string(pages_no_raw.text.strip())
        if len(pages_no) == 2:
            pages_no = Utils.get_valid_value(pages_no_raw)
            pages_no: list[str] = Utils.get_numbers_from_string(pages_no)
            pages_no = min(pages_no)
            return pages_no

class IndeedCountriesTransformer(Transformer):
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

