from typing import Optional, AsyncGenerator, Generator
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from models.job_platform_model import JobPlatformDim
from pipeline.utilities.utils import Utils
from pipeline.common.etls_common import Extractor
from transformers.scrappers.indeed.countries_transformer import IndeedCountriesTransformer

class DateDimensionsGenerator(Extractor):
    
    def extract(self, start_date: str, end_date: str) -> pd.DataFrame:
        dates_dim_df: pd.DataFrame = self.get_date_dimensions(start_date, end_date)
        return dates_dim_df
        
    def get_date_dimensions(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Get the list of countries supported by indeed"""
        dates_dim_df = pd.DataFrame({"date": pd.date_range(start=start_date, end=end_date)})
        dates_dim_df["day"] = dates_dim_df["date"].dt.day_of_week
        dates_dim_df["day_name"] = dates_dim_df["date"].dt.day_name()
        dates_dim_df["week"] = dates_dim_df["date"].dt.isocalendar().week
        dates_dim_df["month"] = dates_dim_df["date"].dt.month
        dates_dim_df["month"] = dates_dim_df["date"].dt.month_name()
        dates_dim_df["quarter"] = dates_dim_df["date"].dt.quarter
        dates_dim_df["year"] = dates_dim_df["date"].dt.year
        dates_dim_df["year_half"] = dates_dim_df["date"].dt.month.apply(lambda x: 1 if x <= 6 else 2)
        return dates_dim_df
