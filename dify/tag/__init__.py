from dify.http import AdminClient
from .schemas import Tag, TagType
from typing import List


class DifyTag:
    def __init__(self, admin_client: AdminClient) -> None:
        self.admin_client = admin_client

    async def list(self, type: TagType) -> List[Tag]:
        """获取指定类型的标签列表

        Args:
            type: 标签类型，可选值包括"app"（应用标签）和"knowledge"（知识库标签）

        Returns:
            List[Tag]: 标签对象列表

        Raises:
            ValueError: 当标签类型无效时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not type:
            raise ValueError("标签类型不能为空")

        # 发送GET请求获取标签列表
        response_data = await self.admin_client.get("/tags", params={"type": type.value})
        
        # 将响应数据转换为Tag对象列表
        return [Tag(**tag_data) for tag_data in response_data]


__all__ = ["DifyTag"]
