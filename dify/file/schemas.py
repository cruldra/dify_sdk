from typing import Optional

from pydantic import BaseModel, Field


class UploadFile(BaseModel):
    """文件上传响应Schema

    Attributes:
        id: 文件ID
        name: 文件名
        size: 文件大小
        extension: 文件扩展名
        mime_type: 文件MIME类型
        created_by: 创建者
        created_at: 创建时间
    """

    id: str = Field(description="文件ID")
    name: str = Field(description="文件名")
    size: int = Field(description="文件大小")
    extension: str = Field(description="文件扩展名")
    mime_type: str = Field(description="文件MIME类型")
    created_by: Optional[str] = Field(default=None, description="创建者")
    created_at: Optional[int] = Field(default=None, description="创建时间")

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


__all__ = ["UploadFile"] 