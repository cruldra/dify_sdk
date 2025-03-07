# Dify SDK - 文件模块示例

本目录包含使用Dify SDK的文件模块的示例代码。

## 示例列表

1. [文件上传](./upload.py) - 展示如何上传文件到Dify平台

## 使用方法

### 环境准备

在运行示例之前，请确保您已经设置了必要的环境变量：

```bash
# .env文件
DIFY_ADMIN_KEY=your_admin_api_key
DIFY_BASE_URL=your_dify_base_url  # 例如：https://api.dify.ai 或您的自托管URL
```

### 运行示例

使用以下命令运行示例：

```bash
# 文件上传示例
python examples/file/upload.py
```

## 文件模块功能

文件模块提供了以下功能：

- `upload(file_path, source)` - 上传文件到Dify平台
  - `file_path`: 要上传的文件路径
  - `source`: 文件来源，默认为"datasets"，可选值包括"datasets"、"app"等

## 数据结构

### FileUploadResponse

文件上传响应的数据结构：

```python
class FileUploadResponse(BaseModel):
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
``` 