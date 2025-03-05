from dify.http import AdminClient
from ..schemas import ApiKey, OperationResult
from .schemas import (
    Conversation,
    ConversationListQueryPayloads,
    ConversationList,
    ConversationRenamePayloads,
    MessageListQueryPayloads,
    MessageList,
    MessageFeedbackPayloads,
)


class DifyConversation:
    def __init__(self, admin_client: AdminClient) -> None:
        self.admin_client = admin_client

    async def find_list(
        self, api_key: ApiKey, payloads: ConversationListQueryPayloads
    ) -> ConversationList:
        """获取对话列表

        Args:
            api_key: API密钥
            payloads: 查询参数配置

        Returns:
            ConversationList: 对话列表对象

        Raises:
            ValueError: 当API密钥为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not api_key:
            raise ValueError("API密钥不能为空")

        api_client = self.admin_client.create_api_client(api_key.token)

        # 准备请求参数
        params = payloads.model_dump(exclude_none=True)

        # 发送请求获取对话列表
        response_data = await api_client.get(
            "/conversations",
            params=params,
        )

        return ConversationList.model_validate(response_data)

    async def get_messages(
        self, api_key: ApiKey, payloads: MessageListQueryPayloads
    ) -> MessageList:
        """获取消息列表

        Args:
            api_key: API密钥
            payloads: 查询参数配置

        Returns:
            MessageList: 消息列表对象

        Raises:
            ValueError: 当API密钥为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not api_key:
            raise ValueError("API密钥不能为空")

        api_client = self.admin_client.create_api_client(api_key.token)

        # 准备请求参数
        params = payloads.model_dump(exclude_none=True)

        # 发送请求获取消息列表
        response_data = await api_client.get(
            "/messages",
            params=params,
        )

        return MessageList.model_validate(response_data)

    async def delete(
        self, api_key: ApiKey, conversation_id: str, user_id: str
    ) -> OperationResult:
        """删除Dify会话

        Args:
            api_key: API密钥
            conversation_id: 会话ID
            user_id: 用户ID

        Returns:
            OperationResult: 操作结果对象

        Raises:
            ValueError: 当API密钥为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not api_key:
            raise ValueError("API密钥不能为空")

        if not conversation_id:
            raise ValueError("会话ID不能为空")

        if not user_id:
            raise ValueError("用户ID不能为空")

        api_client = self.admin_client.create_api_client(api_key.token)

        # 发送删除请求
        response_data = await api_client.delete(
            f"/conversations/{conversation_id}",
            params={"user": user_id},
        )

        return OperationResult(result="success")

    async def rename(
        self,
        api_key: ApiKey,
        conversation_id: str,
        payloads: ConversationRenamePayloads,
    ) -> Conversation:
        """重命名Dify会话

        Args:
            api_key: API密钥
            conversation_id: 会话ID
            payloads: 重命名请求参数配置

        Returns:
            Conversation: 会话对象

        Raises:
            ValueError: 当API密钥为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not api_key:
            raise ValueError("API密钥不能为空")

        if not conversation_id:
            raise ValueError("会话ID不能为空")

        api_client = self.admin_client.create_api_client(api_key.token)

        # 准备请求参数
        json_data = payloads.model_dump(exclude_none=True)

        # 发送请求重命名会话
        response_data = await api_client.post(
            f"/conversations/{conversation_id}/name",
            json=json_data,
        )

        return Conversation.model_validate(response_data)

    async def submit_feedback(
        self,
        api_key: ApiKey,
        message_id: str,
        payloads: MessageFeedbackPayloads,
    ) -> OperationResult:
        """提交消息反馈

        Args:
            api_key: API密钥
            message_id: 消息ID
            payloads: 反馈请求参数配置

        Returns:
            OperationResult: 操作结果对象

        Raises:
            ValueError: 当API密钥为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not api_key:
            raise ValueError("API密钥不能为空")

        if not message_id:
            raise ValueError("消息ID不能为空")

        api_client = self.admin_client.create_api_client(api_key.token)

        # 准备请求参数
        json_data = payloads.model_dump(exclude_none=True)

        # 发送请求提交反馈
        response_data = await api_client.post(
            f"/messages/{message_id}/feedbacks",
            json=json_data,
        )

        return OperationResult.model_validate(response_data)
