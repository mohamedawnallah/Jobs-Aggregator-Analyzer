from typing import Optional, AsyncGenerator, Generator
import pandas as pd
import bs4
from bs4 import BeautifulSoup
from models.job_platform_model import JobPlatformDim
from models.country_model import CountryDim
from pipeline.utilities.utils import Utils

from transformers.scrappers.indeed.countries_transformer import IndeedCountriesTransformer

class JobPlatformsGenerator:
    def get_job_platforms(self, job_platforms_configs: dict[str, str]) -> Generator[JobPlatformDim, None, None]:
        """Get the list of countries supported by indeed"""
        for job_platform_name, job_platform_attributes in job_platforms_configs.items():
            job_platform_url = job_platform_attributes['url']
            job_platform: JobPlatformDim = JobPlatformDim(name=job_platform_name, url=job_platform_url)
            yield job_platform
        
    def get_job_platforms_df(self, job_platforms_generator: AsyncGenerator[JobPlatformDim,None]) -> pd.DataFrame:
        job_platforms_df: Optional[pd.DataFrame] = None
        indx = 1
        for job_platform in job_platforms_generator:
            if indx == 1:
                job_platforms_df = pd.DataFrame(job_platform.to_dict(), index=[indx])
            else:
                new_job_platforms_df = pd.DataFrame(job_platform.to_dict(), index=[indx])
                job_platforms_df = pd.concat([job_platforms_df, new_job_platforms_df],axis=0)
            indx += 1
        return job_platforms_df
