    
from dataclasses import dataclass

@dataclass(frozen=True)
class LightCastCredentials:
    """LightCast Credentials Data Class"""
    lightcast_client_id: str
    lightcast_secret: str
    lightcast_grant_type: str
    lightcast_scope: str
