from typing import List, Callable
import pandas as pd
from pipeline.common.transformers_common import Transformer, DataFrameTransformer
from pipeline.utilities.dataframe_utils import DataFrameUtils
from pipeline.utilities.utils import Utils

class FactlessFactTableTransformer(Transformer, DataFrameTransformer):
    """Indeed Basic Job Info Transformer"""
    
    @staticmethod
    def transform(jobs_dim_df: pd.DataFrame, dates_dim_df: pd.DataFrame, locations_dim_df: pd.DataFrame, companies_dim_df: pd.DataFrame) -> pd.DataFrame:
        """Merge the metadata and data dataframes"""
        # jobs_date_merged_df: pd.DataFrame = pd.merge(jobs_dim_df, dates_dim_df, on='date', how='left')
        companies_locations_merged_df = pd.merge(companies_dim_df, locations_dim_df, on=["city", "country"], how='left')
        jobs_locations_merged_df: pd.DataFrame = pd.merge(jobs_dim_df, locations_dim_df, on=["city", "country_code"], how='left')
        jobs_companies_locations_df: pd.DataFrame = pd.merge(jobs_locations_merged_df, companies_locations_merged_df, on="company_name", how='left')
        # TODO DROP ALL COLUMNS EXCET FOREIGN KEYS IN FACT TABLE
        # TODO HANDLE NULL VALUES IN FOREIGN KEYS IN FACT TABLE 

    
    # @staticmethod
    # def transform_df(fortune_companies_df: pd.DataFrame) -> pd.DataFrame:
    #     """Transform the basic job company info to a namedtuple"""
    #     fortune_companies_df = DataFrameUtils.shift_index_df(fortune_companies_df)
    #     fortune_companies_df = DataFrameUtils.set_index_column_name(fortune_companies_df, 'fortune_company_id')
    #     column_names = DataFrameUtils.get_column_names(fortune_companies_df)
    #     normalize_text_callback = Utils.get_normalized_text
    #     fortune_companies_df_transformed = DataFrameUtils.transform_columns_df(fortune_companies_df, column_names, normalize_text_callback)
    #     return fortune_companies_df_transformed
