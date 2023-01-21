from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from loguru import logger

@dataclass(frozen=True)
class JobBasicInfo:
    """Job Basic Info Data Class"""
    platform_id: str
    title: str
    url: str
    posted_date: str
    city: str
    country: str
    company_name: str
    company_job_platform_url: str
    is_remote: bool

@dataclass(frozen=True)
class JobMoreInfo:
    """Job More Info Data Class"""
    description: str
    benefits: str
    
@dataclass(frozen=True)
class JobDim:
    """Job Full Info Data class"""
    job_basic_info: JobBasicInfo
    job_more_info: JobMoreInfo
    
    def to_dict(self):
        """Convert to dict"""
        job_dim: dict=  {
            **vars(self.job_basic_info),
            **vars(self.job_more_info),
        }
        return job_dim
