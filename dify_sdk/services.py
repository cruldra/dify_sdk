from typing import List, Optional
from .schemas import App, Pagination, DifyAppMode
import logging
import httpx

# 创建日志记录器
logger = logging.getLogger("dify_sdk")


class DifyAPIException(Exception):
    """Dify API 调用异常

    Attributes:
        status_code: HTTP 状态码
        detail: 错误详情
    """

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Dify API 错误 (状态码: {status_code}): {detail}")


class DifyClient:
    def __init__(
        self, base_url: str = None, app_key: str = None, admin_key: str = None
    ):
        self.base_url = base_url or "https://api.dify.ai"
        self.app_key = app_key
        self.admin_key = admin_key


class AppService:
    def __init__(self, client: DifyClient):
        self.client = client

    async def get_app(self, app_id: str) -> App:
        pass

    async def get_apps(self, 
                page: int = 1, 
                limit: int = 100, 
                mode: Optional[DifyAppMode] = None,
                name: str = "",
                is_created_by_me: bool = False) -> Pagination[App]:
        """从 Dify 分页获取应用列表
        
        Args:
            page: 页码，默认为1
            limit: 每页数量限制，默认为100
            mode: 应用模式过滤，可选
            name: 应用名称过滤，默认为空字符串
            is_created_by_me: 是否只返回由我创建的应用，默认为False
            
        Returns:
            Pagination[App]: 分页的应用列表
            
        Raises:
            DifyAPIException: 当API调用失败时抛出
        """
        headers = {
            "Authorization": f"Bearer {self.client.admin_key}",
            "Content-Type": "application/json",
        }

        params = {
            "page": page,
            "limit": limit,
            "name": name,
            "is_created_by_me": is_created_by_me,
        }
        
        if mode:
            params["mode"] = mode.value
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.client.base_url}/console/api/apps",
                    params=params,
                    headers=headers,
                )
                
                response.raise_for_status()
                
                return Pagination[App].model_validate(response.json())
            
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            error_text = e.response.text
            
            logger.error(f"查询Dify应用列表失败")
            logger.error(f"错误码: {status_code}")
            logger.error(f"错误信息: {error_text}")
            
            raise DifyAPIException(
                status_code=status_code,
                detail=f"Failed to fetch apps from Dify: {error_text}"
            )
        except httpx.RequestError as e:
            logger.error(f"查询Dify应用列表请求异常: {str(e)}")
            
            raise DifyAPIException(
                status_code=500,
                detail=f"Request error when fetching apps from Dify: {str(e)}"
            )
