from os import access
import requests
import json
import aiohttp
class LightCastAccessTokenGenerator:
    """LightCast Access Token Generator"""

    @staticmethod
    async def get_access_token(access_token_api, lightcast_grant_type, lightcast_client_id, lightcast_secret, lightcast_scope) -> str:
        """Get the access token"""
        auth_endpoint: str = access_token_api["url"]
        method_type: str = access_token_api["method_type"]
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data: dict = {
            "grant_type": lightcast_grant_type,
            "client_id": lightcast_client_id,
            "client_secret": lightcast_secret,
            "scope": lightcast_scope
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            access_token_response = await session.request(method=method_type,url=auth_endpoint,data=data)
            access_token_response_text = await access_token_response.text()
            access_token: str = json.loads(access_token_response_text)["access_token"]
        return access_token