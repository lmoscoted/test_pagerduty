import requests
from aiohttp import ClientSession

class PagerDutyAPI:
    def __init__(self, base_url, token_api):
        self.base_url = base_url
        self.token_api = token_api

    async def _get_headers(self):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.token_api:
            headers["Authorization"] = f"Token token={self.token_api}"
        return headers
    
    async def _get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        headers = await self._get_headers()
        params = params or {}

        try:
            async with ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    response.raise_for_status()  # Raise exception for non-2xx status codes
                    return await response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error retrieving data: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    async def get_incidents(self, limit=25, offset=0):
        return await self._get("incidents", params={"limit": limit, "offset": offset})

    async def get_services(self, limit=25, offset=0):
        return await self._get("services", params={"limit": limit, "offset": offset})

    async def get_teams(self, limit=25, offset=0):
        return await self._get("teams", params={"limit": limit, "offset": offset})

    async def get_escalation_policies(self, limit=25, offset=0):
        return await self._get("escalation_policies", params={"limit": limit, "offset": offset})
    
    async def _fetch_with_pagination(self, endpoint, limit=25, offset=0):
            data = []
            more = True

            while more:
                response = await self._get(endpoint, params={"limit": limit, "offset": offset})
                data.extend(response[endpoint])
                more = response["more"]
                offset += limit

            return data

    async def fetch_incidents_with_pagination(self):
        return await self._fetch_with_pagination("incidents")

    async def fetch_services_with_pagination(self):
        return await self._fetch_with_pagination("services")

    async def fetch_teams_with_pagination(self):
        return await self._fetch_with_pagination("teams")

    async def fetch_escalation_policies_with_pagination(self):
        return await self._fetch_with_pagination("escalation_policies")