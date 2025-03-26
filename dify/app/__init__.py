import json
from typing import AsyncGenerator

from .conversation import DifyConversation
from .schemas import (
    ApiKey,
    App,
    ChatCompletionResponse,
    ChatPayloads,
    ConversationEvent,
    ConversationEventType,
    ModelConfig,
    RunWorkflowPayloads,
    AppMode,
    AppParameters,
    OperationResult,
)
from .utils import parse_event
from .workflow import DifyWorkflow
from ..http import AdminClient
from ..schemas import Pagination


class DifyApp:
    def __init__(self, admin_client: AdminClient) -> None:
        self.admin_client = admin_client
        self.conversation = DifyConversation(admin_client)
        self.workflow = DifyWorkflow(admin_client)

    async def find_list(
            self,
            page: int = 1,
            limit: int = 100,
            mode: AppMode = None,
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
            params["mode"] = mode.value

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
        api_keys_data = (
            response_data.get("data", [])
            if isinstance(response_data, dict)
            else response_data
        )
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

    async def chat_block(
            self, key: ApiKey | str, payloads: ChatPayloads
    ) -> ChatCompletionResponse:
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
        api_client = self.admin_client.create_api_client(
            key.token if isinstance(key, ApiKey) else key
        )
        # 准备请求数据
        request_data = payloads.model_dump(exclude_none=True)

        return ChatCompletionResponse(**await api_client.post(
            f"/chat-messages", json=request_data, timeout=60
        ))

    async def chat(
            self, key: ApiKey | str, payloads: ChatPayloads
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
        api_client = self.admin_client.create_api_client(
            key.token if isinstance(key, ApiKey) else key
        )
        # 准备请求数据
        request_data = payloads.model_dump(exclude_none=True)

        # 设置请求头
        headers = {
            "Accept": "text/event-stream",
        }

        # 使用API客户端发送流式请求
        full_bytes = b""
        async for chunk in api_client.stream(
                f"/chat-messages", headers=headers, json=request_data
        ):
            full_bytes += chunk
            full_content = full_bytes.decode()
            if full_content == "event: ping\n\n":
                full_bytes = b""
                continue
            # 确保事件块的完整性,以data:开头,以\n\n结尾
            if full_content.startswith("data:") and full_content.endswith("\n\n"):
                # 一个完整的事件块中可能包含多个事件
                for line in full_content.split("\n\n"):
                    if line.startswith("data: "):
                        event_data = json.loads(line[6:])
                        event = parse_event(event_data)
                        yield event
                full_bytes = b""

    async def completion(
            self, api_key: ApiKey | str, payloads: RunWorkflowPayloads
    ) -> AsyncGenerator[ConversationEvent, None]:
        """使用应用进行补全,适用`App.mode`为`completion`的应用.

        Args:
            api_key: API密钥
            payloads: 聊天请求配置

        Returns:
            AsyncGenerator[ConversationEvent, None]: 异步生成器，返回事件数据

        Raises:
            ValueError: 当请求参数无效时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not api_key:
            raise ValueError("API密钥不能为空")

        api_client = self.admin_client.create_api_client(
            api_key.token if isinstance(api_key, ApiKey) else api_key
        )

        # 准备请求数据
        request_data = payloads.model_dump(exclude_none=True)

        # 设置请求头
        headers = {
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }

        # 使用API客户端发送流式请求
        full_bytes = b""
        async for chunk in api_client.stream(
                "/completion-messages",
                method="POST",
                headers=headers,
                json=request_data,
        ):
            full_bytes += chunk
            full_content = full_bytes.decode()
            if full_content == "event: ping\n\n":
                full_bytes = b""
                continue
            if full_content.startswith("data:") and full_content.endswith("\n\n"):
                for line in full_content.split("\n\n"):
                    if line.startswith("data: "):
                        event_data = json.loads(line[6:])
                        event = parse_event(event_data)
                        yield event
                full_bytes = b""

    async def run(
            self, api_key: ApiKey | str, payloads: RunWorkflowPayloads
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

        api_client = self.admin_client.create_api_client(
            api_key.token if isinstance(api_key, ApiKey) else api_key
        )

        # 准备请求数据
        request_data = payloads.model_dump(exclude_none=True)

        # 设置请求头
        headers = {
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }

        # 使用API客户端发送流式请求
        full_bytes = b""
        async for chunk in api_client.stream(
                "/workflows/run",
                json=request_data,
                headers=headers,
        ):
            full_bytes += chunk
            full_content = full_bytes.decode()
            if full_content == "event: ping\n\n":
                full_bytes = b""
                continue
            if full_content.startswith("data:") and full_content.endswith("\n\n"):
                for line in full_content.split("\n\n"):
                    if line.startswith("data: "):
                        event_data = json.loads(line[6:])
                        event = parse_event(event_data)
                        yield event
                full_bytes = b""

    async def get_parameters(self, api_key: ApiKey | str) -> AppParameters:
        """获取应用参数配置

        Args:
            api_key: API密钥对象或密钥字符串

        Returns:
            AppParameters: 应用参数配置对象
        """
        # 处理API密钥参数
        api_client = self.admin_client.create_api_client(
            api_key.token if isinstance(api_key, ApiKey) else api_key
        )
        # 发送请求获取应用参数
        response = await api_client.get(
            f"/parameters",
            headers={"Content-Type": "application/json"},
        )

        # 解析响应数据并返回AppParameters对象
        return AppParameters.model_validate(response)

    async def stop_message(
            self, api_key: ApiKey | str, task_id: str, user_id: str
    ) -> OperationResult:
        """停止消息生成

        Args:
            api_key: API密钥
            task_id: 任务ID
            user_id: 用户ID

        Returns:
            OperationResult: 操作结果对象

        Raises:
            ValueError: 当API密钥、任务ID或用户ID为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        return await self.conversation.stop_message(api_key, task_id, user_id)

    async def update_model_config(
            self, app_id: str, model_config: ModelConfig
    ) -> OperationResult:
        """更新应用的模型配置

        Args:
            app_id: 应用ID
            model_config: 模型配置更新数据

        Returns:
            OperationResult: 操作结果对象

        Raises:
            ValueError: 当应用ID为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not app_id:
            raise ValueError("应用ID不能为空")

        # 发送请求更新模型配置
        response_data = await self.admin_client.post(
            f"/apps/{app_id}/model-config",
            json=model_config.model_dump(by_alias=True, exclude_none=True),
        )

        # 返回操作结果
        return OperationResult(**response_data)

    async def create(
            self,
            name: str,
            mode: AppMode | str,
            description: str = "",
            icon_type: str = "emoji",
            icon: str = "🤖",
            icon_background: str = "#FFEAD5",
    ) -> App:
        """创建新应用

        Args:
            name: 应用名称
            mode: 应用模式，可以是AppMode枚举或字符串
            description: 应用描述
            icon_type: 图标类型
            icon: 图标
            icon_background: 图标背景色

        Returns:
            App: 创建的应用对象

        Raises:
            ValueError: 当应用名称或模式为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not name:
            raise ValueError("应用名称不能为空")

        if not mode:
            raise ValueError("应用模式不能为空")

        payload = {
            "name": name,
            "mode": mode.value if isinstance(mode, AppMode) else mode,
            "description": description,
            "icon_type": icon_type,
            "icon": icon,
            "icon_background": icon_background,
        }

        response_data = await self.admin_client.post("/apps", json=payload)

        return App.model_validate(response_data)

    async def delete(self, app_id: str) -> bool:
        """删除应用

        Args:
            app_id: 应用ID

        Returns:
            bool: 删除成功返回True

        Raises:
            ValueError: 当应用ID为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not app_id:
            raise ValueError("应用ID不能为空")

        # 发送DELETE请求删除应用
        await self.admin_client.delete(f"/apps/{app_id}")

        # 根据curl命令返回204状态码，表示删除成功
        return True


__all__ = [
    "DifyApp",
]
