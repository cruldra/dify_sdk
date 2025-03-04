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



