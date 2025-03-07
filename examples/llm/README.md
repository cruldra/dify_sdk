# Dify SDK - LLM模块示例

本目录包含使用Dify SDK的LLM模块的示例代码。

## 示例列表

1. [获取LLM模型列表](./find_list.py) - 展示如何获取Dify支持的所有LLM模型列表

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
# 获取LLM模型列表
python examples/llm/find_list.py
```

## LLM模块功能

LLM模块提供了以下功能：

- `find_list()` - 获取Dify支持的所有LLM模型列表

## 数据结构

### LLMList

LLM模型列表的数据结构：

```python
class LLMList(BaseModel):
    """LLM模型列表Schema

    Attributes:
        data: 模型列表
    """
    data: list[LLM] = Field(description="模型列表")
```

### LLM

单个LLM模型提供者的数据结构：

```python
class LLM(BaseModel):
    """LLM模型提供者Schema

    Attributes:
        tenant_id: 租户ID
        provider: 模型提供者
        label: 模型标签，包含中英文
        icon_small: 小图标，包含中英文
        icon_large: 大图标，包含中英文
        status: 模型状态
        models: 模型列表
    """
    tenant_id: str = Field(description="租户ID")
    provider: str = Field(description="模型提供者")
    label: MultiLanguage = Field(description="模型标签，包含中英文")
    icon_small: MultiLanguage = Field(description="小图标，包含中英文")
    icon_large: MultiLanguage = Field(description="大图标，包含中英文")
    status: str = Field(description="模型状态")
    models: list[Model] = Field(description="模型列表")
``` 