from typing import Optional
import pandas as pd
import bs4
from pipeline.common.transformers_common import DataFrameTransformer
from pipeline.utilities.utils import Utils
from pipeline.models.country_model import CountryDim
from pipeline.utilities.dataframe_utils import DataFrameUtils

class DateDimensionsTransformer(DataFrameTransformer):
    """Countries Transformer Abstract Class"""
    @staticmethod
    def transform_df(date_dimensions_df: pd.DataFrame):
        cols = list(date_dimensions_df.columns)
        cols.insert(0, cols.pop(cols.index('date_id')))
        date_dimensions_df = date_dimensions_df.reindex(columns= cols)
        return date_dimensions_df