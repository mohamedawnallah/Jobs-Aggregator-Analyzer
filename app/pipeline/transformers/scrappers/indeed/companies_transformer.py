class IndeedCompanyBasicInfoTransformer(Transformer):
    """Indeed Basic Job Info Transformer"""
    @staticmethod
    def transform(company_basic_info: CompanyBasicInfo) -> CompanyBasicInfo:
        """Transform the basic job company info to a namedtuple"""
        company_name = Utils.get_valid_value(company_basic_info.company_name)
        company_name_url = Utils.get_valid_value(company_basic_info.company_name_url)
        company_location = Utils.get_valid_value(company_basic_info.company_location)
        company_rating = Utils.get_valid_value(company_basic_info.company_rating)
        company_country_name = Utils.get_valid_value(company_basic_info.company_country_name)
        company_jobs_platform_url = IndeedTransformerUtils.get_company_url(company_basic_info.company_jobs_platform_url, company_name_url)
        comany_basic_info: namedtuple = CompanyBasicInfo(company_name=company_name,company_rating=company_rating,company_jobs_platform_url=company_jobs_platform_url,company_location=company_location,company_country_name=company_country_name, company_name_url=company_name_url)
        return comany_basic_info

    
class IndeedCompanyMoreBasicInfoTransformer(Transformer):
    """Indeed Basic Job Info Transformer"""
    @staticmethod
    def transform(company_basic_info: CompanyMoreBasicInfo) -> CompanyBasicInfo:
        """Transform the basic job company info to a namedtuple"""
        company_founded_year = Utils.get_valid_value(company_basic_info.company_founded_year)
        company_employees_size = Utils.get_valid_value(company_basic_info.company_employees_size)
        company_revenue = Utils.get_valid_value(company_basic_info.company_revenue)
        company_industry = Utils.get_valid_value(company_basic_info.company_industry)
        company_website = Utils.get_valid_value(company_basic_info.company_website)
        company_more_basic_info: CompanyBasicInfo = CompanyMoreBasicInfo(company_founded_year=company_founded_year,company_employees_size=company_employees_size,company_revenue=company_revenue,company_industry=company_industry,company_website=company_website)
        return company_more_basic_info
    
    
    
class IndeedCompanyTransformer(Transformer):
    """Indeed Company Transformer"""

    @staticmethod
    def transform(jobs_series_df: pd.Series, companies: List[dict]) -> str:
        """Transform Full Job Info"""
        for company in companies:
            if company['company_name_found'] == jobs_series_df['company_name']:
                jobs_series_df['company_city'] = company['company_city']
                jobs_series_df['company_state'] = company['company_state']
                jobs_series_df['company_postal_code'] = company['company_postal_code']
                jobs_series_df['company_naics'] = company['company_naics']
                jobs_series_df['company_original_website'] = company['company_original_website']
                jobs_series_df['is_company_staffing'] = company['is_company_staffing']
                jobs_series_df['is_company_fortune_1000'] = company['is_company_fortune_1000']
                break
        return jobs_series_df
        


