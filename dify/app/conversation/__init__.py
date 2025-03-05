from dify.http import AdminClient
from ..schemas import ApiKey
from .schemas import ConversationListQueryPayloads, ConversationList, MessageListQueryPayloads, MessageList


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
