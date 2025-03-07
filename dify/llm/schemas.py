from typing import Optional
from pydantic import BaseModel, Field


class MultiLanguage(BaseModel):
    """标签Schema

    Attributes:
        en: 英文标签
        zh: 中文标签
    """

    zh_Hans: Optional[str] = Field(description="中文标签")
    en_US: Optional[str] = Field(description="英文标签")


class ModelProperties(BaseModel):
    """模型属性Schema

    Attributes:
        max_tokens: 最大令牌数
        temperature: 温度
    """

    context_size: Optional[int] = Field(description="上下文大小")
    mode: Optional[str] = Field(description="模式")


class Model(BaseModel):
    """LLM模型Schema

    Attributes:
        model: 模型名称
        label: 模型标签，包含中英文
        model_type: 模型类型
        features: 模型支持的功能列表
        fetch_from: 模型来源
        model_properties: 模型属性
        deprecated: 是否已弃用
        status: 模型状态
        load_balancing_enabled: 是否启用负载均衡
    """

    model: str = Field(description="模型名称")
    label: MultiLanguage = Field(description="模型标签，包含中英文")
    model_type: str = Field(description="模型类型")
    features: list[str] = Field(description="模型支持的功能列表")
    fetch_from: str = Field(description="模型来源")
    model_properties: ModelProperties = Field(description="模型属性")
    deprecated: bool = Field(default=False, description="是否已弃用")
    status: str = Field(description="模型状态")
    load_balancing_enabled: bool = Field(default=False, description="是否启用负载均衡")

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class LLM(BaseModel):
    """LLM模型提供者Schema

    Attributes:
        tenant_id: 租户ID
        provider: 模型提供者
        label: 模型标签，包含中英文
        icon_small: 小图标，包含中英文
        icon_large: 大图标，包含中英文
        status: 模型状态
    """

    tenant_id: str = Field(description="租户ID")
    provider: str = Field(description="模型提供者")
    label: MultiLanguage = Field(description="模型标签，包含中英文")
    icon_small: MultiLanguage = Field(description="小图标，包含中英文")
    icon_large: MultiLanguage = Field(description="大图标，包含中英文")
    status: str = Field(description="模型状态")
    models: list[Model] = Field(description="模型列表")
    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class LLMList(BaseModel):
    """LLM模型列表Schema

    Attributes:
        data: 模型列表
        total: 模型总数
    """

    data: list[LLM] = Field(description="模型列表")
