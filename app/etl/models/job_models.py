from dataclasses import dataclass, field
from etl.models.company_models import CompanyBasicInfo, CompanyMoreBasicInfo


@dataclass(frozen=True)
class JobBasicInfo:
    """Job Basic Info Data Class"""
    job_id: str
    job_title: str
    job_url: str
    job_salary: str

@dataclass(frozen=True)
class JobMoreInfo:
    """Job More Info Data Class"""
    job_description: str
    job_benefits: str
    job_posted_date: str
    job_skills: str = field(default="N/A")

@dataclass(frozen=True)
class JobCompanyBasicInfo:
    """Job Company BasicInfo Data class"""
    job_basic_info: JobBasicInfo
    company_basic_info: CompanyBasicInfo
    company_more_basic_info: CompanyMoreBasicInfo

@dataclass(frozen=True)
class JobFullInfo:
    """Job Full Info Data class"""
    job_basic_info: JobBasicInfo
    company_basic_info: CompanyBasicInfo
    company_more_basic_info: CompanyMoreBasicInfo
    job_more_info: JobMoreInfo
    # company_more_info: CompanyMoreInfo

    def to_dict(self):
        """Convert to dict"""
        job_full_info: dict=  {
            **vars(self.job_basic_info),
            **vars(self.company_basic_info),
            **vars(self.company_more_basic_info),
            **vars(self.job_more_info)
        }
        return job_full_info

@dataclass(frozen=True)
class JobCountry:
    """Job Country"""
    country_name: str
    country_jobs_url: str

