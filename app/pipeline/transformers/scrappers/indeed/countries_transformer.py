from typing import Optional
import pandas as pd
import bs4
from pipeline.common.transformers_common import Transformer, DataFrameTransformer
from pipeline.utilities.dataframe_utils import  DataFrameUtils
from pipeline.utilities.utils import Utils
from pipeline.models.country_model import CountryDim

class IndeedCountriesTransformer(Transformer, DataFrameTransformer):
    """Countries Transformer Abstract Class"""
    @staticmethod
    def transform(country: bs4.element.Tag) -> CountryDim:
        """Transform the country name"""
        country_name: str = Utils.get_text(country)
        country_link: str = IndeedCountriesTransformer.get_country_link(country)
        country_code = IndeedCountriesTransformer.get_country_code(country_link)
        country: CountryDim = CountryDim(country_name=country_name, country_code=country_code, country_url=country_link)
        return country
    
    @staticmethod
    def get_country_link(country: bs4.element.Tag) -> str:
        country_link: Optional[str] = Utils.get_attribute_value_from_tag(country, 'a', 'href')
        return country_link
    
    @staticmethod
    def get_country_code(country_link: str) -> str:
        country_code = country_link.split("//")[1].split(".")[0]
        return country_code
    
    @staticmethod
    def transform_df(countries_df: pd.DataFrame):
        countries_df = DataFrameUtils.drop_id_column(countries_df, 'country_id')
        countries_df = DataFrameUtils.set_index_column_name(countries_df, 'country_id')
        column_names = DataFrameUtils.get_column_names(countries_df)
        normalize_text_callback = Utils.get_normalized_text
        countries_df = DataFrameUtils.transform_columns_df(countries_df, column_names, normalize_text_callback)
        return countries_df
    
    