from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, computed_field
from ..schemas import RetrieverResource


class Conversation(BaseModel):
    id: str = Field(description="会话ID")
    name: str = Field(description="会话名称")
    inputs: dict = Field(description="用户输入参数")
    status: str = Field(description="会话状态")
    introduction: str = Field(description="开场白")
    created_at: int = Field(description="创建时间戳")
    updated_at: int = Field(description="更新时间戳")


class ConversationList(BaseModel):
    data: List[Conversation] = Field(description="会话列表")
    has_more: bool = Field(description="是否有更多数据")
    limit: int = Field(description="实际返回数量")


class SortBy(str, Enum):
    CREATED_AT_ASC = "created_at"
    CREATED_AT_DESC = "-created_at"
    UPDATED_AT_ASC = "updated_at"
    UPDATED_AT_DESC = "-updated_at"


class ConversationListQueryPayloads(BaseModel):
    """会话列表查询参数配置

    Attributes:
        user (str): 用户标识，由开发者定义规则，需保证用户标识在应用内唯一
        last_id (str): （选填）当前页最后面一条记录的 ID，默认 null
        limit (int): （选填）一次请求返回多少条记录，默认 20 条，最大 100 条，最小 1 条
        sort_by (str): （选填）排序字段，默认 -updated_at(按更新时间倒序排列)
    """

    user: str = Field(description="用户标识，需保证在应用内唯一")
    last_id: Optional[str] = Field(default=None, description="当前页最后一条记录的ID")
    limit: Optional[int] = Field(default=20, ge=1, le=100, description="返回记录数量")
    sort_by: Optional[str] = Field(
        default=SortBy.UPDATED_AT_DESC.value,
        description="排序字段，可选值：created_at, -created_at, updated_at, -updated_at",
    )

    # Pydantic V2 配置方式
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),  # 可选，解决 Pydantic 保留名称冲突
    }


class MessageListQueryPayloads(BaseModel):
    """消息列表查询参数配置

    Attributes:
        conversation_id (str): 会话ID
        user (str): 用户标识，由开发者定义规则，需保证用户标识在应用内唯一
        first_id (str): （选填）当前页第一条聊天记录的ID，默认null
        limit (int): （选填）一次请求返回多少条聊天记录，默认20条
    """

    conversation_id: str = Field(description="会话ID")
    user: str = Field(description="用户标识，需保证在应用内唯一")
    first_id: Optional[str] = Field(
        default=None, description="当前页第一条聊天记录的ID"
    )
    limit: Optional[int] = Field(default=20, description="返回聊天记录数量")

    # Pydantic V2 配置方式
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),  # 可选，解决 Pydantic 保留名称冲突
    }


class MessageFile(BaseModel):
    """消息文件
    
    Attributes:
        id (Optional[str]): 文件ID
        type (Optional[str]): 文件类型
        url (Optional[str]): 预览地址
        belongs_to (Optional[str]): 文件归属方
        filename (Optional[str]): 文件名
        mime_type (Optional[str]): MIME类型
        size (Optional[int]): 文件大小
        transfer_method (Optional[str]): 传输方式
    """
    id: Optional[str] = Field(default=None, description="文件ID")
    type: Optional[str] = Field(default=None, description="文件类型")
    url: Optional[str] = Field(default=None, description="预览地址")
    belongs_to: Optional[str] = Field(default=None, description="文件归属方")
    filename: Optional[str] = Field(default=None, description="文件名")
    mime_type: Optional[str] = Field(default=None, description="MIME类型")
    size: Optional[int] = Field(default=None, description="文件大小")
    transfer_method: Optional[str] = Field(default=None, description="传输方式")


class AgentThought(BaseModel):
    """Agent思考
    
    Attributes:
        id (Optional[str]): 思考ID
        message_id (Optional[str]): 消息ID
        position (Optional[int]): 思考位置
        thought (Optional[str]): 思考内容
        observation (Optional[str]): 工具返回结果
        tool (Optional[str]): 使用工具
        tool_input (Optional[str]): 工具输入参数
        message_files (Optional[List[MessageFile]]): 关联文件ID
    """
    id: Optional[str] = Field(default=None, description="思考ID")
    message_id: Optional[str] = Field(default=None, description="消息ID")
    position: Optional[int] = Field(default=None, description="思考位置")
    thought: Optional[str] = Field(default=None, description="思考内容")
    observation: Optional[str] = Field(default=None, description="工具返回结果")
    tool: Optional[str] = Field(default=None, description="使用工具")
    tool_input: Optional[str] = Field(default=None, description="工具输入参数")
    message_files: Optional[List[MessageFile]] = Field(
        default_factory=list, description="关联文件ID"
    )


class Feedback(BaseModel):
    rating: Optional[str] = Field(default=None, description="用户反馈")


class Message(BaseModel):
    """消息
    
    Attributes:
        id (Optional[str]): 消息ID
        conversation_id (Optional[str]): 会话ID
        inputs (Optional[dict]): 输入参数
        query (Optional[str]): 用户提问
        message_files (Optional[List[MessageFile]]): 消息文件
        agent_thoughts (Optional[List[AgentThought]]): Agent思考过程
        answer (Optional[str]): 回答内容
        created_at (Optional[int]): 创建时间
        feedback (Optional[Feedback]): 用户反馈
        retriever_resources (Optional[List[RetrieverResource]]): 检索资源
    """
    id: Optional[str] = Field(default=None, description="消息ID")
    conversation_id: Optional[str] = Field(default=None, description="会话ID")
    inputs: Optional[dict] = Field(default_factory=dict, description="输入参数")
    query: Optional[str] = Field(default=None, description="用户提问")
    message_files: Optional[List[MessageFile]] = Field(
        default_factory=list, description="消息文件"
    )
    agent_thoughts: Optional[List[AgentThought]] = Field(
        default_factory=list, description="Agent思考过程"
    )
    answer: Optional[str] = Field(default=None, description="回答内容")
    created_at: Optional[int] = Field(default=None, description="创建时间")
    feedback: Optional[Feedback] = Field(
        default_factory=Feedback, description="用户反馈"
    )
    retriever_resources: Optional[List[RetrieverResource]] = Field(
        default_factory=list, description="检索资源"
    )

    @computed_field
    @property
    def created_time(self) -> Optional[str]:
        date = datetime.fromtimestamp(self.created_at) if self.created_at else None
        return date.strftime("%Y-%m-%d %H:%M:%S") if date else None

    model_config = {"arbitrary_types_allowed": True, "protected_namespaces": ()}
class MessageList(BaseModel):
    """消息列表

    Attributes:
        data (List[Message]): 消息列表
        has_more (bool): 是否有更多数据
        limit (int): 实际返回数量
    """
    data: Optional[List[Message]] = Field(
        default_factory=list, description="消息列表"
    )
    has_more: Optional[bool] = Field(default=False, description="是否有更多数据")
    limit: Optional[int] = Field(default=20, description="实际返回数量")


class ConversationRenamePayloads(BaseModel):
    """会话重命名请求模型"""

    name: Optional[str] = Field(default=None, description="新会话名称")
    auto_generate: Optional[bool] = Field(default=False, description="是否自动生成标题")
    user: str = Field(description="用户标识")


class MessageFeedbackPayloads(BaseModel):
    """消息反馈请求模型"""

    rating: Optional[str] = Field(
        None,
        description="点赞 like, 点踩 dislike, 撤销点赞 null",
        examples=["like", "dislike", None],
    )
    user: str = Field(..., description="用户标识")
    content: Optional[str] = Field(
        None, description="反馈的具体信息", examples=["这个回答很有帮助"]
    )