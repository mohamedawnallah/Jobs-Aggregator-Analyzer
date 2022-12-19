import pandas as pd
from typing import List, Callable, Optional

class DataFrameUtils:
    
    @staticmethod
    def drop_id_column(df: pd.DataFrame, id_column: str) -> pd.DataFrame:
        """Drop the id column from the dataframe"""
        df = df.drop(id_column, axis=1, inplace=False)
        return df
    
    @staticmethod
    def set_index_column_name(df: pd.DataFrame, index_column_name: str) -> pd.DataFrame:
        """Set the index column name"""
        df.index.name = index_column_name
        return df

    @staticmethod
    def get_column_names(df: pd.DataFrame) -> List[str]:
        """Get the column names of the dataframe"""
        column_names: List[str] = df.columns.tolist()
        return column_names
    @staticmethod
    def transform_columns_df(df: pd.DataFrame, column_names: List[str], transform_function: Callable) -> pd.DataFrame:
        """Transform the columns of the dataframe"""
        for column_name in column_names:
            df = DataFrameUtils.transform_column_df(df, column_name, transform_function)
        return df
    
    @staticmethod
    def transform_column_df(df: pd.DataFrame, column_name: str, transform_function: Callable) -> pd.DataFrame:
        """Transform the column of the dataframe"""
        df[column_name] = df[column_name].apply(transform_function)
        return df
    
    @staticmethod
    def shift_index_df(df: pd.DataFrame, step: Optional[int] = 1) -> pd.DataFrame:
        """Shift the index of the dataframe"""
        df.index = df.index + step
        return df
  