from typing import List, Callable
import pandas as pd
from pipeline.common.transformers_common import Transformer, DataFrameTransformer
from pipeline.utilities.dataframe_utils import DataFrameUtils
from pipeline.utilities.utils import Utils

class FortuneCompaniesAPITransformer(Transformer, DataFrameTransformer):
    """Indeed Basic Job Info Transformer"""
    @staticmethod
    def transform(fortune_companies_info: List[dict]) -> pd.DataFrame:
        """Merge the metadata and data dataframes"""
        fortune_companies_columns_meta_data, fortune_companies_data = fortune_companies_info
        fortune_companies_columns_df: pd.DataFrame = FortuneCompaniesAPITransformer.get_columns_df(fortune_companies_columns_meta_data)
        fortune_companies_data_df: pd.DataFrame = FortuneCompaniesAPITransformer.get_data_df(fortune_companies_data)
        fortune_companies_transformed_df: pd.DataFrame = FortuneCompaniesAPITransformer.transform_fortune_companies(fortune_companies_columns_df, fortune_companies_data_df)
        return fortune_companies_transformed_df
    
    @staticmethod
    def get_columns_df(fortune_companies_columns_meta_data: dict):
        fortune_companies_columns: List[dict] = fortune_companies_columns_meta_data["sortable"] + fortune_companies_columns_meta_data["filterable"]
        fortune_companies_columns: List[str] = [column["importField"] for column in fortune_companies_columns]
        fortune_companies_columns_df: pd.DataFrame = pd.DataFrame(columns=fortune_companies_columns)
        return fortune_companies_columns_df

    @staticmethod
    def get_data_df(fortune_companies_data: dict) -> pd.DataFrame:
        """Get the data for the dataframe"""
        fortune_companies_data_df: pd.DataFrame = pd.DataFrame(fortune_companies_data["items"])
        return fortune_companies_data_df

    @staticmethod
    def transform_fortune_companies(fortune_companies_columns_df: pd.DataFrame, fortune_companies_data_df: pd.DataFrame) -> pd.DataFrame:
        """Merge the metadata and data dataframes"""
        fortune_companies_merged_df: pd.DataFrame = pd.concat([fortune_companies_columns_df, fortune_companies_data_df], axis=1)
        fortune_companies_fields_transformer_callback: Callable = FortuneCompaniesAPITransformer.transform_fortune_companies_fields
        fortune_companies_transformed_df = fortune_companies_merged_df.apply(fortune_companies_fields_transformer_callback,axis=1)
        fortune_companies_transformed_df = fortune_companies_transformed_df.drop(columns=["fields","title"])
        return fortune_companies_transformed_df
    
    @staticmethod
    def transform_fortune_companies_fields(fortune_company_series: pd.Series) -> pd.DataFrame:
        """Transform the Fortune 1000 Companies dataframe"""
        fortune_company_fields: List[dict] = fortune_company_series["fields"]
        for company_field in fortune_company_fields:
            column: str = company_field["key"]
            column_value: str = company_field["value"]
            fortune_company_series[column] = column_value
        return fortune_company_series
    
    @staticmethod
    def transform_df(fortune_companies_df: pd.DataFrame) -> pd.DataFrame:
        """Transform the basic job company info to a namedtuple"""
        fortune_companies_df = DataFrameUtils.shift_index_df(fortune_companies_df)
        fortune_companies_df = DataFrameUtils.set_index_column_name(fortune_companies_df, 'fortune_company_id')
        column_names = DataFrameUtils.get_column_names(fortune_companies_df)
        normalize_text_callback = Utils.get_normalized_text
        fortune_companies_df_transformed = DataFrameUtils.transform_columns_df(fortune_companies_df, column_names, normalize_text_callback)
        return fortune_companies_df_transformed