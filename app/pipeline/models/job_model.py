from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from loguru import logger

@dataclass(frozen=True)
class JobBasicInfo:
    """Job Basic Info Data Class"""
    job_platform_id: str
    job_title: str
    job_url: str
    job_posted_date: str
    job_city: str
    is_job_remote: bool
    company_name: str
    company_job_platform_url: str
    
@dataclass(frozen=True)
class JobMoreInfo:
    """Job More Info Data Class"""
    job_description: str
    job_benefits: str
    
@dataclass(frozen=True)
class JobDim:
    """Job Full Info Data class"""
    job_basic_info: JobBasicInfo
    job_more_info: JobMoreInfo
    country_id: int
    job_id: Optional[int] = field(default=None)

    def to_dict(self):
        """Convert to dict"""
        job_dim: dict=  {
            'job_id': self.job_id,
            'country_id': self.country_id,
            **vars(self.job_basic_info),
            **vars(self.job_more_info),
        }
        return job_dim

