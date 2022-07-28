from dataclasses import dataclass

@dataclass
class Country:
    """Company Data Class"""
    country_name: str
    country_code: str

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
    job_skills: str

@dataclass(frozen=True)
class CompanyBasicInfo:
    """Company Basic Info"""
    company_name: str
    company_location: str
    company_rating: str
    company_url: str
    company_country_name: str

@dataclass(frozen=True)
class JobCompanyBasicInfo:
    """Job Company BasicInfo Data class"""
    job_basic_info: JobBasicInfo
    company_basic_info: CompanyBasicInfo

@dataclass(frozen=True)
class JobFullInfo:
    """Job Full Info Data class"""
    job_basic_info: JobBasicInfo
    company_basic_info: CompanyBasicInfo
    job_more_info: JobMoreInfo

    def to_dict(self):
        """Convert to dict"""
        job_full_info: dict=  {
            **vars(self.job_basic_info),
            **vars(self.company_basic_info),
            **vars(self.job_more_info)
        }
        return job_full_info
