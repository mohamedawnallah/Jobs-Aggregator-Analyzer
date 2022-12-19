from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class CountryDim:
    """Company Data Class"""
    country_name: str
    country_code: str
    country_url: str
    country_id: Optional[int] = field(default=None)
    
    def to_dict(self):
        """Convert to dict"""
        country_dim: dict=  {
            'country_id': self.country_id,
            'country_name': self.country_name,
            'country_code': self.country_code,
            'country_url': self.country_url,
        }
        return country_dim