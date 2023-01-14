from typing import List, Callable
import pandas as pd
from pipeline.common.transformers_common import Transformer, DataFrameTransformer
from pipeline.utilities.dataframe_utils import DataFrameUtils
from models.company_model import Company
from pipeline.utilities.utils import Utils

class CompaniesInfoAPITransformer(Transformer):
    """Indeed Basic Job Info Transformer"""
    @staticmethod
    def transform(companies_info_data: List[dict]) -> pd.DataFrame:
        """Merge the metadata and data dataframes"""
        company_models: List[Company] = CompaniesInfoAPITransformer.get_company_models(companies_info_data)
        companies_df: pd.DataFrame = CompaniesInfoAPITransformer.get_companies_df(company_models)
        companies_transformed_df: pd.DataFrame = CompaniesInfoAPITransformer.transform_df(companies_df)
        return companies_transformed_df
        
        
    @staticmethod
    def get_company_models(companies_info_data: List[dict]) -> List[Company]:
        company_models = []
        for company in companies_info_data:
            if company["companies"]:
                company_name = company.get("company_name_job_platform", None)
                company = company["companies"][0]
                city = None if not company.get("city", {}) else company.get("city", {}).get("name", None)
                longitude = None if not company.get("city", {}) else company.get("city", {}).get("longitude", None)
                latitude = None if not company.get("city", {}) else company.get("city", {}).get("latitude", None)
                country = None if not company.get("country", {}) else company.get("country", {}).get("nameEn", None)
                continent = None if not company.get("continent", {}) else company.get("continent", {}).get("nameEn", None)
                revenue = company.get("revenue", None)
                revenue_exact = company.get("revenueExact", None)
                industry_main = company.get("industryMain", None)
                alexa_rank = company.get("alexaRank", None)
                monthly_visitors = company.get("monthlyVisitors", None)
                stock_exchange = company.get("stockExchange", None)
                is_unicorn_company = company.get("isUnicornCompany", None)
                total_employees_exact = company.get("totalEmployeesExact", None)
                total_employees = company.get("totalEmployees", None)
                year_founded = company.get("yearFounded", None)
                description_short = company.get("descriptionShort", None)
                description = company.get("description", None)
                domain = company.get("domain", None)
                industries = ", ".join(company.get("industries", None))
                technologies = ", ".join(company.get("technologies", None))
                technologies_categories = ", ".join(company.get("technologyCategories", None))
                companies_subsidiaries = CompaniesInfoAPITransformer.get_names_joined(company.get("companiesSubsidiaries", None))
                companies_acquisitions = CompaniesInfoAPITransformer.get_names_joined(company.get("companiesAcquisitions", None))
                companies_similar = CompaniesInfoAPITransformer.get_names_joined(company.get("companiesSimilar", None)) 
                social_networks = CompaniesInfoAPITransformer.get_values_key_joined(company.get("socialNetworks", None))
                company_model = Company(name=company_name, city=city, longitude=longitude, latitude=latitude, country=country, continent=continent,
                                revenue=revenue,revenue_exact= revenue_exact, industry_main=industry_main, industries=industries,
                                companies_subsidiaries=companies_subsidiaries, companies_acquisitions=companies_acquisitions,
                                companies_similar=companies_similar, alexa_rank=alexa_rank, monthly_visitors=monthly_visitors,
                                social_networks=social_networks, stock_exchange=stock_exchange, technologies_categories=technologies_categories,
                                technologies=technologies, is_unicorn_company=is_unicorn_company, total_employees_exact=total_employees_exact,
                                total_employees=total_employees, year_founded=year_founded, description_short=description_short,
                                description=description, domain=domain)
                company_models.append(company_model)
        return company_models
        
    @staticmethod
    def get_names_joined(values: List[dict]) -> str:
        if not values:
            return None
        names = [value.get("name", None) for value in values]
        names = ", ".join(names)
        return names

    @staticmethod
    def get_values_key_joined(key: dict) -> str:
        if not key:
            return None
        values = [value for value in key.values()]
        values = ", ".join(values)
        return values
    
    @staticmethod
    def get_companies_df(company_models: List[Company]) -> pd.DataFrame:
        companies_df = pd.DataFrame([company.__dict__ for company in company_models])
        return companies_df

    
    @staticmethod
    def transform_df(companies_df: pd.DataFrame) -> pd.DataFrame:
        """Transform the basic job company info to a namedtuple"""     
        companies_df = DataFrameUtils.shift_index_df(companies_df)
        companies_df = DataFrameUtils.set_index_column_name(companies_df, 'company_id')
        # column_names = DataFrameUtils.get_column_names(companies_df)
        # normalize_text_callback = Utils.get_normalized_text
        # companies_df_transformed = DataFrameUtils.transform_columns_df(companies_df, column_names, normalize_text_callback)
        return companies_df
    
    