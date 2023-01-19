from pipeline.common.transformers_common import Transformer
from typing import List
import pandas as pd
from datetime import datetime, timedelta
from pipeline.utilities.utils import Utils
from pipeline.utilities.dataframe_utils import DataFrameUtils
from models.job_model import JobBasicInfo, JobMoreInfo
from pipeline.common.transformers_common import Transformer, DataFrameTransformer

class IndeedJobBasicInfoTransformer(DataFrameTransformer, Transformer):
    """Indeed Basic Job Info Transformer"""
    @staticmethod
    def transform(job_basic_info: JobBasicInfo, company_base_url: str) -> JobBasicInfo:
        """Transform the basic job company info to a namedtuple"""
        job_title = Utils.get_text(job_basic_info.job_title)
        job_platform_id = Utils.get_text(job_basic_info.job_platform_id)
        company_name = Utils.get_text(job_basic_info.company_name)
        company_job_platform_url = Utils.get_text(job_basic_info.company_job_platform_url)
        job_posted_date = Utils.get_text(job_basic_info.job_posted_date)
        job_city = Utils.get_text(job_basic_info.job_city)
        
        job_platform_id = IndeedJobBasicInfoTransformer.get_job_platform_id_normalized(job_platform_id)
        company_job_platform_url = IndeedJobBasicInfoTransformer.get_company_url(company_base_url, company_job_platform_url)
        job_posted_date_formated = IndeedJobBasicInfoTransformer.get_job_posted_date_formated(job_posted_date)
        job_url = IndeedJobBasicInfoTransformer.get_job_url(job_basic_info.job_url, job_platform_id)
        job_city = IndeedJobBasicInfoTransformer.get_job_city_normalized(job_city=job_city)
        is_job_remote = IndeedJobBasicInfoTransformer.is_job_remote(job_city=job_city, job_title=job_title)
        
        job_basic_info = JobBasicInfo(job_title=job_title,job_platform_id=job_platform_id,job_posted_date=job_posted_date_formated,job_url=job_url, company_name=company_name, company_job_platform_url=company_job_platform_url, job_city=job_city, is_job_remote=is_job_remote, job_country=job_basic_info.job_country)
        return job_basic_info

    @staticmethod
    def get_job_platform_id_normalized(job_id: str):
        """Get a valid job id"""
        valid_job_id = job_id.split("jk=")[-1].split("&")[0]
        return valid_job_id

    @staticmethod
    def get_job_url(job_base_url: str, job_id: str) -> str:
        """Get the job link from job id"""
        job_url = job_base_url % {"job_id": job_id}
        return job_url

    @staticmethod
    def get_company_url(company_base_url: str, company_job_platform_url: str) -> str:
        """Get the company website from company name"""
        company_job_platform_url = "N/A" if not company_job_platform_url else company_job_platform_url
        company_name_in_url = company_job_platform_url.split('/')[-1]
        company_job_platform_url = company_base_url % {"company_name": company_name_in_url}
        company_job_platform_url = company_job_platform_url.replace(" ", "%20")
        return company_job_platform_url
    
    @staticmethod
    def get_job_posted_date_formated(job_posted_date: str, date_format: str = "%Y/%m/%d") -> str:
        job_posted_date = job_posted_date.lower()
        if "today" in job_posted_date or "just" in job_posted_date:
            job_posted_date = datetime.today().strftime(date_format)
            return job_posted_date
        specific_days_ago_mentioned: List[int] = Utils.get_digits_from_string(job_posted_date)
        if not specific_days_ago_mentioned:
            time_difference = datetime.today() - timedelta(days=30)
        else:
            time_difference = datetime.today() - timedelta(days=specific_days_ago_mentioned[0])
        job_posted_date = time_difference.strftime(date_format)
        return job_posted_date
        
    @staticmethod
    def get_job_city_normalized(job_city: str):
        job_city = job_city.lower()
        job_city = job_city.split(",")[0]
        return job_city
    
    @staticmethod
    def is_job_remote(job_city: str, job_title: str):
        job_city = job_city.lower().strip()
        job_title = job_title.lower().strip()
        if "remote" in job_city or "remote" in job_title:
            return True
        return False
    
class IndeedJobMoreInfoTransformer(Transformer):
    """Indeed More Job Info Transformer Abstract Class"""
    @staticmethod
    async def transform(job_info: JobMoreInfo) -> JobMoreInfo:
        """Transform the more job info"""
        job_description: str = Utils.get_text(job_info.job_description)
        job_benefits: str = IndeedJobMoreInfoTransformer.get_job_benefits_normalized(job_info.job_benefits)
        job_more_info = JobMoreInfo(job_description=job_description,job_benefits=job_benefits)
        return job_more_info

    @staticmethod
    def get_job_benefits_normalized(benefits_section) -> str:
        """Get the benefits"""
        result = (None if not benefits_section else benefits_section.find_all("div", class_="css-1f2yqp0 e1xnxm2i0"))
        all_benefits = None
        if result:
            all_benefits = IndeedJobMoreInfoTransformer.transform_job_benefits(result)
        return all_benefits

    @staticmethod
    def transform_job_benefits(benefits_raw: str) -> str:
        """Getting jobs benefits mentioned in job indeed page"""
        benefits_str = ""
        for benefit in benefits_raw:
            benefit_value = Utils.get_text(benefit)
            benefits_str += benefit_value + ", "
        return benefits_str


class IndeedJobsTransformer(DataFrameTransformer):
    @staticmethod
    def transform_df(jobs_df: pd.DataFrame):
        jobs_df = DataFrameUtils.drop_id_column(jobs_df, "job_id")
        jobs_df = DataFrameUtils.set_index_column_name(jobs_df, "job_id")
        jobs_df = DataFrameUtils.shift_index_df(jobs_df, 1)
        column_names = DataFrameUtils.get_column_names(jobs_df)
        normalize_text_callback = Utils.get_normalized_text
        jobs_df = DataFrameUtils.transform_columns_df(jobs_df, column_names, normalize_text_callback)
        jobs_df = IndeedJobsTransformer.transform_job_posted_date_df(jobs_df)
        return jobs_df
    
    @staticmethod
    def transform_job_posted_date_df(jobs_df: pd.DataFrame):
        jobs_df["job_posted_date"] = pd.to_datetime(jobs_df["job_posted_date"], format="%Y/%m/%d")
        return jobs_df
    
    