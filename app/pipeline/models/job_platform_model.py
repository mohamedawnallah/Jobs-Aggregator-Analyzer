from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class JobPlatformDim:
    """Company Data Class"""
    name: str
    url: str
    job_platform_id: Optional[int] = field(default=None)
    
    def to_dict(self):
        """Convert to dict"""
        job_platform_dim: dict=  {
            'job_platform_id': self.job_platform_id,
            'name': self.name,
            'url': self.url,
        }
        return job_platform_dim