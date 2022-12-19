from typing import Optional
import pandas as pd
import bs4
from pipeline.common.transformers_common import DataFrameTransformer
from pipeline.utilities.utils import Utils
from pipeline.models.country_model import CountryDim

class JobPlatformsTransformer(DataFrameTransformer):
    """Countries Transformer Abstract Class"""
    @staticmethod
    def transform_df(job_platforms_df: pd.DataFrame):
        job_platforms_df.drop('job_platform_id', axis=1, inplace=True)
        job_platforms_df.index.name = "job_platform_id"
        for column in job_platforms_df.columns:
            if column != job_platforms_df.index.name:
                job_platforms_df[column] = job_platforms_df[column].apply(lambda row: Utils.get_normalized_text(text=row))
        return job_platforms_df