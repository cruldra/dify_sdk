import httpx


class HttpClient:
    def __init__(self, base_url: str, key: str):
        self.base_url = base_url
        self.key = key
        self.headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }


    async def get(self, url: str, params: dict = None, headers: dict = None):
        async with httpx.AsyncClient() as client:
            merged_headers = self.headers.copy()
            if headers:
                merged_headers.update(headers)
                
            response = await client.get(
                self.base_url + url, params=params, headers=merged_headers
            )
            return response.json()


class AdminClient(HttpClient):
    def __init__(self, base_url: str, key: str):
        super().__init__(base_url + "/console/api", key)


class ApiClient(HttpClient):
    def __init__(self, base_url: str, key: str):
        super().__init__(base_url, key)
