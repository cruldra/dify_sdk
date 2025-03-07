from pydantic import BaseModel, Field
from typing import List, Optional

from enum import Enum

class TagType(str, Enum):
    """标签类型枚举"""
    APP = "app"
    KNOWLEDGE = "knowledge"


class Tag(BaseModel):
    """标签"""

    id: str = Field(..., description="标签唯一标识")
    name: str = Field(..., description="标签名称")
    type: TagType = Field(..., description="标签类型")
    binding_count: int = Field(..., description="绑定数量")

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }
