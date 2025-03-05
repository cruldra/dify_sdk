import json
from typing import AsyncGenerator, Any

import httpx

from .schemas import ApiKey, App, ChatPayloads, ConversationEvent, ConversationEventType, RunWorkflowPayloads
from .utils import parse_event
from ..http import AdminClient
from ..schemas import Pagination


class DifyApp:
    def __init__(self, admin_client: AdminClient) -> None:
        self.admin_client = admin_client

    async def find_list(
        self,
        page: int = 1,
        limit: int = 100,
        mode: str = None,
        name: str = "",
        is_created_by_me: bool = False,
    ):
        """从 Dify 分页获取应用列表

        Args:
            page: 页码，默认为1
            limit: 每页数量限制，默认为100
            mode: 应用模式过滤，可选
            name: 应用名称过滤，默认为空字符串
            is_created_by_me: 是否只返回由我创建的应用，默认为False

        Returns:
            Pagination[App]: 分页的应用列表
        """

        params = {
            "page": page,
            "limit": limit,
            "name": name,
            "is_created_by_me": is_created_by_me,
        }

        if mode:
            params["mode"] = mode

        response_data = await self.admin_client.get(
            "/apps",
            params=params,
        )

        return Pagination[App].model_validate(response_data)

    async def find_by_id(self, app_id: str) -> App:
        """根据ID从Dify获取单个应用详情

        Args:
            app_id: 应用ID

        Returns:
            App: 应用详情对象

        Raises:
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        response_data = await self.admin_client.get(f"/apps/{app_id}")
        return App.model_validate(response_data)

    async def get_keys(self, app_id: str) -> list[ApiKey]:
        """获取应用的API密钥列表

        Args:
            app_id: 应用ID

        Returns:
            list[ApiKey]: API密钥列表，包含每个密钥的详细信息

        Raises:
            httpx.HTTPStatusError: 当API请求失败时抛出
            ValueError: 当应用ID为空时抛出
        """
        if not app_id:
            raise ValueError("应用ID不能为空")

        response_data = await self.admin_client.get(f"/apps/{app_id}/api-keys")
        # 确保返回的数据是列表格式
        api_keys_data = response_data.get("data", []) if isinstance(response_data, dict) else response_data
        return [ApiKey.model_validate(key) for key in api_keys_data]

    async def create_api_key(self, app_id: str) -> ApiKey:
        """创建API密钥

        Args:
            app_id: 应用ID

        Returns:
            ApiKey: 创建的API密钥对象

        Raises:
            httpx.HTTPStatusError: 当API请求失败时抛出
            ValueError: 当应用ID为空时抛出
        """
        if not app_id:
            raise ValueError("应用ID不能为空")

        response_data = await self.admin_client.post(f"/apps/{app_id}/api-keys")
        return ApiKey.model_validate(response_data)

    async def delete_api_key(self, app_id: str, key_id: str) -> bool:
        """删除API密钥

        Args:
            app_id: 应用ID
            key_id: API密钥ID

        Returns:
            bool: 删除是否成功

        Raises:
            httpx.HTTPStatusError: 当API请求失败时抛出
            ValueError: 当应用ID或密钥ID为空时抛出
        """
        if not app_id:
            raise ValueError("应用ID不能为空")
        
        if not key_id:
            raise ValueError("API密钥ID不能为空")

        await self.admin_client.delete(f"/apps/{app_id}/api-keys/{key_id}")
        return True

    async def chat(
        self,  key: ApiKey, payloads: ChatPayloads
    ) -> AsyncGenerator[ConversationEvent, None]:
        """和应用进行对话,适用`App.mode`为`chat`的应用.

        Args:
            key: 应用密钥
            payloads: 聊天请求配置

        Returns:
            AsyncGenerator[ConversationEvent, None]: 异步生成器，返回事件数据

        Raises:
            ValueError: 当请求参数无效时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not key:
            raise ValueError("应用密钥不能为空")
        api_client = self.admin_client.create_api_client(key.token)
        # 准备请求数据
        request_data = payloads.model_dump(exclude_none=True)

        # 设置请求头
        headers = {
            "Accept": "text/event-stream",
        }

        # 使用API客户端发送流式请求
        async for chunk in api_client.stream(
            f"/chat-messages", headers=headers, json=request_data
        ):
            # 解析事件数据
            for line in chunk.decode().split("\n"):
                if line.startswith("data:"):
                    event_data = json.loads(line[5:])
                    # 根据事件类型返回对应的事件对象
                    event = parse_event(event_data)
                    yield event

    async def completion(
        self, app_id: str, payloads: ChatPayloads
    ) -> AsyncGenerator[ConversationEvent, None]:
        """使用应用进行补全,适用`App.mode`为`completion`的应用.

        Args:
            app_id: 应用ID
            payloads: 聊天请求配置

        Returns:
            AsyncGenerator[ConversationEvent, None]: 异步生成器，返回事件数据

        Raises:
            ValueError: 当请求参数无效时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not app_id:
            raise ValueError("应用ID不能为空")

        if not payloads.query and not payloads.inputs:
            raise ValueError("消息内容和inputs不能同时为空")

        # 准备请求数据
        request_data = payloads.model_dump(exclude_none=True)

        # 设置请求头
        headers = {
            "Accept": "text/event-stream",
        }

        try:
            # 使用API客户端发送流式请求
            async for chunk in self.api_client.stream(
                f"/completion-messages",
                method="POST",
                headers=headers,
                json=request_data,
            ):
                # 解析事件数据
                for line in chunk.decode("utf-8").split("\n"):
                    if line.startswith("data:"):
                        try:
                            event_data = json.loads(line[5:])
                            # 根据事件类型返回对应的事件对象
                            event_type = event_data.get("event")
                            if event_type:
                                # 直接使用事件数据构建事件对象
                                yield event_data
                        except Exception as e:
                            # 忽略无法解析的数据
                            continue
        except httpx.HTTPStatusError as e:
            # 处理HTTP错误
            error_content = await e.response.aread()
            raise ValueError(
                f"请求失败，状态码: {e.response.status_code}, 错误信息: {error_content.decode('utf-8')}"
            )
        except Exception as e:
            # 处理其他异常
            raise ValueError(f"发送消息时发生错误: {str(e)}")

    async def run(
        self, api_key: ApiKey, payloads: RunWorkflowPayloads
    ) -> AsyncGenerator[ConversationEvent, None]:
        """使用应用运行工作流,适用`App.mode`为`workflow`的应用.

        Args:
            api_key: API密钥
            payloads: 工作流请求配置

        Returns:
            AsyncGenerator[ConversationEvent, None]: 异步生成器，返回事件数据

        Raises:
            ValueError: 当请求参数无效时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not api_key:
            raise ValueError("API密钥不能为空")
        
        api_client = self.admin_client.create_api_client(api_key.token)

        # 准备请求数据
        request_data = payloads.model_dump(exclude_none=True)

        # 设置请求头
        headers = {
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }

        # 使用API客户端发送流式请求
        async for chunk in api_client.stream(
            "/workflows/run",
            json=request_data,
            headers=headers,
        ):
            # 解析事件数据
            for line in chunk.decode().split("\n"):
                if line.startswith("data:"):
                    event_data = json.loads(line[5:])
                    # 根据事件类型返回对应的事件对象
                    event = parse_event(event_data)
                    yield event
