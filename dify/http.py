from typing import Any, AsyncGenerator

import httpx


class HttpClient:
    def __init__(self, base_url: str, key: str):
        self.base_url = base_url
        self.key = key
        self.headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }

    async def __merge_headers__(self, headers: dict = None):
        merged_headers = self.headers.copy()
        if headers:
            merged_headers.update(headers)
        return merged_headers

    async def get(
            self, url: str, params: dict = None, headers: dict = None
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            merged_headers = await self.__merge_headers__(headers)

            response = await client.get(
                self.base_url + url, params=params, headers=merged_headers
            )
            response.raise_for_status()
            return response.json()

    async def post(
            self, url: str, json: dict = None, params: dict = None, headers: dict = None
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            merged_headers = await self.__merge_headers__(headers)

            response = await client.post(
                self.base_url + url, json=json, params=params, headers=merged_headers
            )
            response.raise_for_status()
            return response.json()

    async def stream(
            self, url: str, params: dict = None, headers: dict = None, method: str = "POST", json: dict = None
    ) -> AsyncGenerator[bytes, None]:
        async with httpx.AsyncClient() as client:
            merged_headers = await self.__merge_headers__(headers)

            async with client.stream(
                    method, self.base_url + url, params=params, headers=merged_headers, json=json
            ) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes():
                    yield chunk


class AdminClient(HttpClient):
    def __init__(self, base_url: str, key: str):
        self.host_url = base_url
        super().__init__(base_url + "/console/api", key)

    def create_api_client(self, app_key: str):
        return ApiClient(self.host_url, app_key)


class ApiClient(HttpClient):
    def __init__(self, base_url: str, key: str):
        super().__init__(base_url + "/v1", key)
