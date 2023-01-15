from typing import List, Callable, Optional
import pandas as pd
from pipeline.common.transformers_common import Transformer, DataFrameTransformer
from pipeline.utilities.dataframe_utils import DataFrameUtils
from pipeline.utilities.utils import Utils

class FortuneCompaniesInfoTransformer(Transformer, DataFrameTransformer):
    """Indeed Basic Job Info Transformer"""
    
    @staticmethod
    def transform(companies_df: pd.DataFrame, fortune_companies_df: pd.DataFrame) -> pd.DataFrame:
        """Merge the metadata and data dataframes"""
        companies_df: pd.DataFrame = FortuneCompaniesInfoTransformer.lower_case_company_names(companies_df)
        fortune_companies_info_merged_df: pd.DataFrame = FortuneCompaniesInfoTransformer.merge_df(companies_df, fortune_companies_df, common_column="name", join_type="left")
        fortune_companies_info_merged_df: pd.DataFrame = FortuneCompaniesInfoTransformer.transform_df(fortune_companies_info_merged_df)
        return fortune_companies_info_merged_df
        
    @staticmethod
    def lower_case_company_names(companies_df: pd.DataFrame) -> pd.DataFrame:
        """Lower case the company names"""
        companies_df["name"] = companies_df["name"].str.lower()
        return companies_df

    @staticmethod
    def merge_df(companies_df: pd.DataFrame, fortune_companies_df: pd.DataFrame, common_column: str, join_type: str) -> pd.DataFrame:
        """Merge the metadata and data dataframes"""
        fortune_companies_info_merged_df: pd.DataFrame = pd.merge(companies_df, fortune_companies_df, on=common_column, how=join_type)
        return fortune_companies_info_merged_df
    
    @staticmethod
    def transform_df(fortune_companies_info_merged_df: pd.DataFrame) -> pd.DataFrame:
        """Transform the basic job company info to a namedtuple"""
        fortune_companies_info_merged_df = DataFrameUtils.drop_id_column(fortune_companies_info_merged_df,id_column="company_id")
        fortune_companies_info_merged_df = DataFrameUtils.shift_index_df(fortune_companies_info_merged_df)
        fortune_companies_info_merged_df = DataFrameUtils.set_index_column_name(fortune_companies_info_merged_df, 'company_id')
        # column_names = DataFrameUtils.get_column_names(fortune_companies_df)
        # normalize_text_callback = Utils.get_normalized_text
        # fortune_companies_df_transformed = DataFrameUtils.transform_columns_df(fortune_companies_df, column_names, normalize_text_callback)
        return fortune_companies_info_merged_df
