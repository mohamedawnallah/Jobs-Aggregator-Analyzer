from dataclasses import dataclass

@dataclass(frozen=True)
class Company:
    """Company Data Class"""
    name: str
    city: str
    country: str
    longitude: float
    latitude: float
    revenue: str
    revenue_exact: int
    continent: str
    industry_main: str
    industries: str
    companies_subsidiaries: str
    companies_acquisitions: str
    companies_similar: str
    alexa_rank: int
    monthly_visitors: str
    social_networks: str
    stock_exchange: str
    technologies: str
    technologies_categories: str
    is_unicorn_company: bool
    total_employees: str
    total_employees_exact: int
    year_founded: int
    description: str
    description_short: str
    domain: str
    
