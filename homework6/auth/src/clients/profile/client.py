from src.config import PROFILE_CLIENT_URL, PROFILE_CLIENT_TOKEN
from src.clients.http_client import HTTPClient


class ProfileClient(HTTPClient):
    srv_profile_url = '/srv/profile'

    def __init__(self) -> None:
        super().__init__(
            url=PROFILE_CLIENT_URL, # type: ignore
            token=PROFILE_CLIENT_TOKEN,  # type: ignore
        )

    async def create_profile(self, payload):
        response = await self.post(url=self.srv_profile_url, json=payload)
        result = response.json()
        return result