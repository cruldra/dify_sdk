from enum import Enum
from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import computed_field


class DifyAppMode(str, Enum):
    CHAT = "chat"
    AGENT_CHAT = "agent-chat"
    WORKFLOW = "workflow"
    COMPLETION = "completion"


T = TypeVar("T")


class Tag(BaseModel):
    """标签模型

    Attributes:
        id: 标签ID
        name: 标签名称
        type: 标签类型
    """

    id: str = Field(description="标签ID")
    name: str = Field(description="标签名称")
    type: str = Field(description="标签类型")


class ModelConfig(BaseModel):
    """AI应用配置模型"""

    opening_statement: Optional[str] = Field(default=None, description="开场白文本")
    suggested_questions: Optional[List[str]] = Field(
        default=None, description="建议问题列表"
    )
    suggested_questions_after_answer: Optional[dict] = Field(
        default=None, description="回答后的建议问题配置"
    )
    speech_to_text: Optional[dict] = Field(default=None, description="语音转文字配置")
    text_to_speech: Optional[dict] = Field(default=None, description="文字转语音配置")
    retriever_resource: Optional[dict] = Field(default=None, description="检索资源配置")
    annotation_reply: Optional[dict] = Field(default=None, description="注释回复配置")
    more_like_this: Optional[dict] = Field(default=None, description="相似推荐配置")
    sensitive_word_avoidance: Optional[dict] = Field(
        default=None, description="敏感词规避配置"
    )
    external_data_tools: Optional[List[str]] = Field(
        default=None, description="外部数据工具列表"
    )
    model: Optional[dict] = Field(default=None, description="模型配置")
    user_input_form: Optional[List[dict]] = Field(
        default=None, description="用户输入表单配置"
    )
    dataset_query_variable: Optional[str] = Field(
        default=None, description="数据集查询变量"
    )
    pre_prompt: Optional[str] = Field(default=None, description="预设提示词")
    agent_mode: Optional[dict] = Field(default=None, description="代理模式配置")
    prompt_type: Optional[str] = Field(default=None, description="提示类型")
    chat_prompt_config: Optional[dict] = Field(default=None, description="对话提示配置")
    completion_prompt_config: Optional[dict] = Field(
        default=None, description="补全提示配置"
    )
    dataset_configs: Optional[dict] = Field(default=None, description="数据集配置")
    file_upload: Optional[dict] = Field(default=None, description="文件上传配置")
    created_by: Optional[str] = Field(default=None, description="创建者")
    created_at: Optional[int] = Field(default=None, description="创建时间戳")
    updated_by: Optional[str] = Field(default=None, description="更新者")
    updated_at: Optional[int] = Field(default=None, description="更新时间戳")

    # Pydantic V2 配置方式
    model_config = {"populate_by_name": True, "protected_namespaces": ()}


class App(BaseModel):
    """Dify应用模型

    Attributes:
        id: 应用ID
        name: 应用名称
        max_active_requests: 最大活跃请求数
        description: 应用描述
        mode: 应用模式
        icon_type: 图标类型
        icon: 图标
        icon_background: 图标背景
        icon_url: 图标URL
        app_config: 模型配置
        workflow: 工作流
        use_icon_as_answer_icon: 是否使用图标作为回答图标
        created_by: 创建者
        created_at: 创建时间
        updated_by: 更新者
        updated_at: 更新时间
        tags: 标签
    """

    id: Optional[str] = Field(default=None, description="应用ID")
    name: Optional[str] = Field(default=None, description="应用名称")
    max_active_requests: Optional[int] = Field(
        default=None, description="最大活跃请求数"
    )
    description: Optional[str] = Field(default=None, description="应用描述")
    mode: Optional[DifyAppMode] = Field(default=None, description="应用模式")
    icon_type: Optional[str] = Field(default=None, description="图标类型")
    icon: Optional[str] = Field(default=None, description="图标")
    icon_background: Optional[str] = Field(default=None, description="图标背景")
    icon_url: Optional[str] = Field(default=None, description="图标URL")
    app_config: Optional[ModelConfig] = Field(
        default_factory=ModelConfig, alias="model_config", description="模型配置"
    )
    workflow: Optional[dict] = Field(default=None, description="工作流")
    use_icon_as_answer_icon: Optional[bool] = Field(
        default=None, description="是否使用图标作为回答图标"
    )
    created_by: Optional[str] = Field(default=None, description="创建者")
    created_at: Optional[datetime] = Field(default=None, description="创建时间")
    updated_by: Optional[str] = Field(default=None, description="更新者")
    updated_at: Optional[datetime] = Field(default=None, description="更新时间")
    tags: Optional[List[Tag]] = Field(default_factory=list, description="标签")
    monthly_price: Optional[float] = Field(default=None, description="月付价格")
    yearly_price: Optional[float] = Field(default=None, description="年付价格")
    # Pydantic V2 配置方式
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),  # 可选，解决 Pydantic 保留名称冲突
    }


class Pagination(BaseModel, Generic[T]):
    """分页请求模型

    Attributes:
        page: 当前页码
        limit: 每页条数
        total: 总条数
        has_more: 是否有更多数据
        data: 数据列表
    """

    page: int = Field(default=1, description="当前页码")
    limit: int = Field(default=10, description="每页条数")
    total: Optional[int] = Field(default=None, description="总条数")
    has_more: Optional[bool] = Field(default=None, description="是否有更多数据")
    data: Optional[List[T]] = Field(default=None, description="数据列表")


class ChatRequestConfig(BaseModel):
    """聊天请求配置"""

    inputs: Optional[dict] = Field(
        default_factory=dict, description="额外的输入参数配置"
    )
    response_mode: Optional[str] = Field(default="streaming", description="响应模式")
    conversation_id: Optional[str] = Field(default=None, description="对话ID")
    files: Optional[List[str]] = Field(
        default_factory=list, description="上传的文件列表"
    )
    query: Optional[str] = Field(default=None, description="用户输入的问题或指令")
    inputs: Optional[dict] = Field(
        default_factory=dict, description="额外的输入参数配置"
    )
    parent_message_id: Optional[str] = Field(default=None, description="父消息ID")
    app_config: Optional[ModelConfig] = Field(
        default_factory=ModelConfig, alias="model_config", description="模型配置"
    )
    # Pydantic V2 配置方式
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),  # 可选，解决 Pydantic 保留名称冲突
    }


class LoginResponse(BaseModel):
    """登录响应模型"""

    access_token: str
    refresh_token: str


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


class AppQuery(BaseModel):
    """应用搜索参数"""

    keyword: Optional[str] = Field(default=None, description="关键词")
    page: int = Field(1, description="页码，从1开始")
    page_size: int = Field(10, description="每页数量")
    mode: Optional[DifyAppMode] = Field(
        None, description="应用模式，为空时返回所有应用"
    )


class MessageFile(BaseModel):
    id: Optional[str] = Field(default=None, description="文件ID")
    type: Optional[str] = Field(default=None, description="文件类型")
    url: Optional[str] = Field(default=None, description="预览地址")
    belongs_to: Optional[str] = Field(default=None, description="文件归属方")
    filename: Optional[str] = Field(default=None, description="文件名")
    mime_type: Optional[str] = Field(default=None, description="MIME类型")
    size: Optional[int] = Field(default=None, description="文件大小")
    transfer_method: Optional[str] = Field(default=None, description="传输方式")


class AgentThought(BaseModel):
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


class RetrieverResource(BaseModel):
    position: Optional[int] = Field(default=None, description="段落位置")
    document_id: Optional[str] = Field(default=None, description="文档ID")
    content: Optional[str] = Field(default=None, description="内容摘要")


class Feedback(BaseModel):
    rating: Optional[str] = Field(default=None, description="用户反馈")


class MessageItem(BaseModel):
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
    data: Optional[List[MessageItem]] = Field(
        default_factory=list, description="消息列表"
    )
    has_more: Optional[bool] = Field(default=False, description="是否有更多数据")
    limit: Optional[int] = Field(default=20, description="实际返回数量")


class OperationResult(BaseModel):
    """操作结果模型"""

    result: str = Field(default="success", description="操作结果")


class ApiKey(BaseModel):
    """API密钥模型"""

    id: str = Field(description="API密钥ID")
    type: str = Field(description="密钥类型")
    token: str = Field(description="API令牌")
    last_used_at: Optional[int] = Field(default=None, description="最后使用时间戳")
    created_at: Optional[int] = Field(default=None, description="创建时间戳")


class ConversationRenameRequest(BaseModel):
    """会话重命名请求模型"""

    name: Optional[str] = Field(default=None, description="新会话名称")
    auto_generate: Optional[bool] = Field(default=False, description="是否自动生成标题")
    user: str = Field(description="用户标识")


class MessageFeedbackRequest(BaseModel):
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


class AppParameters(BaseModel):
    """应用参数模型"""

    user_input_form: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, description="用户输入表单配置"
    )
    file_upload: Optional[Dict[str, Any]] = Field(
        default=None, description="文件上传配置"
    )
    system_parameters: Optional[Dict[str, Any]] = Field(
        default=None, description="系统参数配置"
    )
