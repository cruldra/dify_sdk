# Dify SDK - 标签模块示例

本目录包含使用Dify SDK的标签模块的示例代码。

## 示例列表

1. [获取标签列表](./list.py) - 展示如何获取Dify标签列表

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
# 获取标签列表示例
python examples/tag/list.py
```

## 标签模块功能

标签模块提供了以下功能：

- `list(type)` - 获取指定类型的标签列表
  - `type`: 标签类型，可选值包括"app"（应用标签）和"dataset"（数据集标签）

## 使用示例

```python
# 初始化AdminClient和DifyTag
admin_client = AdminClient(BASE_URL, API_KEY)
dify_tag = DifyTag(admin_client)

# 获取应用标签列表
app_tags = await dify_tag.list("app")
print(f"找到 {len(app_tags)} 个应用标签")

# 获取数据集标签列表
dataset_tags = await dify_tag.list("dataset")
print(f"找到 {len(dataset_tags)} 个数据集标签")

# 打印标签信息
for tag in app_tags:
    print(f"ID: {tag.id}")
    print(f"名称: {tag.name}")
    print(f"类型: {tag.type}")
    print(f"创建时间: {tag.created_at}")
``` 