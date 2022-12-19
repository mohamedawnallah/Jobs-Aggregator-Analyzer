from typing import Optional
import pandas as pd
import bs4
from pipeline.common.transformers_common import DataFrameTransformer
from pipeline.utilities.utils import Utils
from pipeline.models.country_model import CountryDim

class DateDimensionsTransformer(DataFrameTransformer):
    """Countries Transformer Abstract Class"""
    @staticmethod
    def transform_df(date_dimensions_df: pd.DataFrame):
        date_dimensions_df.index.name = "date_id"
        return date_dimensions_df