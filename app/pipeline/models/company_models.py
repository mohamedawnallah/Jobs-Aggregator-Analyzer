from dataclasses import dataclass

@dataclass(frozen=True)
class CompanyBasicInfo:
    """Company Basic Info"""
    company_name: str
    company_name_url: str
    company_rating: str
    company_location: str
    company_country_name: str
    company_jobs_platform_url: str

@dataclass(frozen=True)
class CompanyReviews:
    """Company Reviews"""
    company_reviews_count: int
    company_reviews_titles: str
    
@dataclass(frozen=True)
class CompanyMoreBasicInfo:
    """Company Basic More Info"""
    company_website: str
    company_industry: str
    company_founded_year: int
    company_employees_size: int
    company_revenue: int
    company_reviews: CompanyReviews

# @dataclass(frozen=True)
# class FortuneCompanyInfo:
#     """Company More Info"""
#     company_name: str
#     company_rank: int
#     company_revenue_percent_change: float
#     company_profits: float
#     company_profits_percent_change: float
#     company_assets: float
#     company_employees_size: float
#     company_change_in_rank: int
#     years_count_on_500_list: int 
#     is_company_fortune_500: bool = field(default=None)