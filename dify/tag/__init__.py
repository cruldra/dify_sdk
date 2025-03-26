from typing import List

from dify.http import AdminClient
from .schemas import Tag, TagType, BindingPayloads


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
        
    async def create(self, name: str, type: TagType) -> Tag:
        """创建新标签

        Args:
            name: 标签名称
            type: 标签类型，可选值包括TagType.APP（应用标签）和TagType.KNOWLEDGE（知识库标签）

        Returns:
            Tag: 创建的标签对象

        Raises:
            ValueError: 当标签名称或类型无效时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not name:
            raise ValueError("标签名称不能为空")
        
        if not type:
            raise ValueError("标签类型不能为空")

        # 准备请求数据
        payload = {
            "name": name,
            "type": type.value
        }

        # 发送POST请求创建标签
        response_data = await self.admin_client.post("/tags", json=payload)
        
        # 返回创建的标签对象
        return Tag(**response_data)
        
    async def bind(self, payload: BindingPayloads) -> bool:
        """绑定标签到目标对象

        Args:
            payload: 标签绑定参数，包含标签ID列表、目标对象ID和标签类型

        Returns:
            bool: 绑定成功返回True

        Raises:
            ValueError: 当参数无效时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not payload.tag_ids:
            raise ValueError("标签ID列表不能为空")
        
        if not payload.target_id:
            raise ValueError("目标对象ID不能为空")
        
        if not payload.type:
            raise ValueError("标签类型不能为空")

        # 发送POST请求绑定标签
        await self.admin_client.post(
            "/tag-bindings/create",
            json=payload.model_dump(by_alias=True, exclude_none=True)
        )
        
        # 绑定成功返回True
        return True
        
    async def delete(self, tag_id: str) -> bool:
        """删除特定标签

        Args:
            tag_id: 标签ID

        Returns:
            bool: 删除成功返回True

        Raises:
            ValueError: 当标签ID为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not tag_id:
            raise ValueError("标签ID不能为空")

        # 发送DELETE请求删除标签
        await self.admin_client.delete(f"/tags/{tag_id}")
        
        # 删除成功返回True
        return True


__all__ = ["DifyTag"]
