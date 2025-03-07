from dify.http import AdminClient
from typing import List, Optional
from .schemas import DataSetCreatePayloads, DataSetCreateResponse, DataSetList

class DifyDataset:
    def __init__(self, admin_client: AdminClient) -> None:
        self.admin_client = admin_client

    async def create(self, payload: DataSetCreatePayloads) -> DataSetCreateResponse:
        """创建新的知识库

        Args:
            payload: 知识库创建参数

        Returns:
            DataSetCreateResponse: 知识库创建响应对象，包含知识库信息和文档列表

        Raises:
            ValueError: 当参数无效时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not payload:
            raise ValueError("知识库创建参数不能为空")

        # 发送POST请求创建知识库
        response_data = await self.admin_client.post(
            "/datasets/init",
            json=payload.model_dump(by_alias=True, exclude_none=True),
        )

        # 返回知识库创建响应对象
        return DataSetCreateResponse(**response_data)

    async def find_list(
        self, 
        page: int = 1, 
        limit: int = 30, 
        include_all: bool = False, 
        tag_ids: Optional[List[str]] = None
    ) -> DataSetList:
        """查询知识库列表

        Args:
            page: 页码，默认为1
            limit: 每页数量，默认为30
            include_all: 是否包含所有知识库，默认为False
            tag_ids: 标签ID列表，用于筛选特定标签的知识库，默认为None

        Returns:
            DataSetList: 知识库列表对象，包含知识库列表、总数和是否有更多

        Raises:
            ValueError: 当参数无效时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if page < 1:
            raise ValueError("页码不能小于1")
        
        if limit < 1:
            raise ValueError("每页数量不能小于1")
        
        # 准备查询参数
        params = {
            "page": page,
            "limit": limit,
            "include_all": str(include_all).lower()
        }
        
        # 如果提供了标签ID列表，则添加到查询参数中
        if tag_ids:
            params["tag_ids"] = ",".join(tag_ids)
        
        # 发送GET请求查询知识库列表
        response_data = await self.admin_client.get("/datasets", params=params)
        
        # 返回知识库列表对象
        return DataSetList(**response_data)

    async def delete(self, dataset_id: str) -> bool:
        """删除知识库

        Args:
            dataset_id: 知识库ID

        Returns:
            bool: 删除成功返回True

        Raises:
            ValueError: 当知识库ID为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not dataset_id:
            raise ValueError("知识库ID不能为空")

        # 发送DELETE请求删除知识库
        await self.admin_client.delete(f"/datasets/{dataset_id}")
        
        # 根据curl命令返回204状态码，表示删除成功
        return True

__all__ = ["DifyDataset"]

