from dify.http import AdminClient
from .schemas import DataSetCreatePayloads, DataSetCreateResponse

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

