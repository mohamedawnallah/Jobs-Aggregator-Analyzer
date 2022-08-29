from typing import List
import pandas as pd
from etl.common.transformers_common import Transformer

class Fortune1000CompaniesTransformer(Transformer):
    """Indeed Basic Job Info Transformer"""
    @staticmethod
    def transform(fortune_1000_companies_meta_data: dict, fortune_1000_companies_data: dict) -> pd.DataFrame:
        """Transform the basic job company info to a namedtuple"""
        fortune_1000_companies_metadata_df: pd.DataFrame = Fortune1000CompaniesTransformer.get_metadata_df(fortune_1000_companies_meta_data)
        fortune_1000_companies_data_df: pd.DataFrame = Fortune1000CompaniesTransformer.get_data_df(fortune_1000_companies_data)
        fortune_1000_companies_transformed_df: pd.DataFrame = Fortune1000CompaniesTransformer.transform_fortune_1000_companies(fortune_1000_companies_metadata_df, fortune_1000_companies_data_df)
        return fortune_1000_companies_transformed_df

    @staticmethod
    def get_metadata_df(fortune_1000_companies_meta_data: dict) -> pd.DataFrame:
        """Get the columns for the dataframe"""
        fortune_1000_companies_raw_columns: List[dict] = fortune_1000_companies_meta_data["sortable"] + fortune_1000_companies_meta_data["filterable"]
        fortune_1000_companies_columns: List[str] = [column["importField"] for column in fortune_1000_companies_raw_columns]
        fortune_1000_companies_metadata_df: pd.DataFrame = pd.DataFrame(columns=fortune_1000_companies_columns)
        return fortune_1000_companies_metadata_df
    
    @staticmethod
    def get_data_df(fortune_1000_companies_data: dict) -> pd.DataFrame:
        """Get the data for the dataframe"""
        fortune_1000_companies_data_df: pd.DataFrame = pd.DataFrame(fortune_1000_companies_data["items"])
        return fortune_1000_companies_data_df

    @staticmethod
    def transform_fortune_1000_companies(fortune_1000_companies_metadata_df: pd.DataFrame, fortune_1000_companies_data_df: pd.DataFrame) -> pd.DataFrame:
        """Merge the metadata and data dataframes"""
        fortune_1000_companies_merged_df: pd.DataFrame = pd.concat([fortune_1000_companies_metadata_df, fortune_1000_companies_data_df], axis=1)
        fortune_1000_companies_transformed_df = fortune_1000_companies_merged_df.apply(Fortune1000CompaniesTransformer._fortune_1000_companies_fields_transformer,axis=1)
        fortune_1000_companies_transformed_df = fortune_1000_companies_transformed_df.drop(columns=["fields","title"])
        return fortune_1000_companies_transformed_df
    
    @staticmethod
    def _fortune_1000_companies_fields_transformer(fortune_1000_company_series: pd.Series) -> pd.DataFrame:
        """Transform the Fortune 1000 Companies dataframe"""
        fortune_1000_company_fields: List[dict] = fortune_1000_company_series["fields"]
        for company_field in fortune_1000_company_fields:
            column: str = company_field["key"]
            column_value: str = company_field["value"]
            fortune_1000_company_series[column] = column_value
        return fortune_1000_company_series
