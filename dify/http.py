import json
from typing import Any, AsyncGenerator, Dict, BinaryIO

import httpx

from .exceptions import DifyException


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
            if response.is_error:
                raise DifyException(
                    f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}"
                )
            return response.json()

    async def post(
            self, url: str, json: dict = None, params: dict = None, headers: dict = None
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            merged_headers = await self.__merge_headers__(headers)

            response = await client.post(
                self.base_url + url, json=json, params=params, headers=merged_headers
            )
            if response.is_error:
                raise DifyException(
                    f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}"
                )
            return response.json()

    async def upload(
            self, url: str, files: Dict[str, tuple[str, BinaryIO]], params: dict = None, headers: dict = None
    ) -> dict[str, Any]:
        """上传文件

        Args:
            url: API路径
            files: 文件字典，格式为 {"file": (filename, file_object)}
            params: 查询参数
            headers: 请求头

        Returns:
            dict: API响应数据

        Raises:
            DifyException: 当API请求失败时抛出
        """
        async with httpx.AsyncClient() as client:
            # 上传文件时不设置Content-Type，让httpx自动设置为multipart/form-data
            auth_headers = {"Authorization": f"Bearer {self.key}"}
            if headers:
                auth_headers.update(headers)

            response = await client.post(
                self.base_url + url, 
                files=files, 
                params=params, 
                headers=auth_headers
            )
            if response.is_error:
                raise DifyException(
                    f"文件上传失败，状态码: {response.status_code}, 错误信息: {response.text}"
                )
            return response.json()

    async def delete(
            self,
            url: str,
            params: dict = None,
            content: dict = None,
            headers: dict = None,
            ret_type: str = None,
    ) -> Any:
        async with httpx.AsyncClient() as client:
            merged_headers = await self.__merge_headers__(headers)

            response = await client.request(
                "DELETE",
                self.base_url + url,
                params=params,
                headers=merged_headers,
                content=json.dumps(content) if content else None,
            )
            if response.is_error:
                raise DifyException(
                    f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}"
                )
            if ret_type == "json":
                return response.json()
            elif ret_type == "text":
                return response.text
            else:
                return None

    async def stream(
            self,
            url: str,
            params: dict = None,
            headers: dict = None,
            method: str = "POST",
            json: dict = None,
    ) -> AsyncGenerator[bytes, None]:
        async with httpx.AsyncClient(timeout=600) as client:
            merged_headers = await self.__merge_headers__(headers)

            async with client.stream(
                    method,
                    self.base_url + url,
                    params=params,
                    headers=merged_headers,
                    json=json,
            ) as response:
                if response.is_error:
                    error_content = await response.aread()
                    raise DifyException(
                        f"请求失败，状态码: {response.status_code}, 错误信息: {error_content.decode('utf-8')}"
                    )
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
