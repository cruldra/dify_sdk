# Dify SDK - 标签模块示例

本目录包含使用Dify SDK的标签模块的示例代码。

## 示例列表

1. [获取标签列表](./list.py) - 展示如何获取Dify标签列表
2. [创建标签](./create.py) - 展示如何创建Dify标签
3. [删除标签](./delete.py) - 展示如何删除Dify标签

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

# 创建标签示例
python examples/tag/create.py

# 删除标签示例
python examples/tag/delete.py
```

## 标签模块功能

标签模块提供了以下功能：

- `list(type)` - 获取指定类型的标签列表
  - `type`: 标签类型，类型为`TagType`枚举，可选值包括`TagType.APP`（应用标签）和`TagType.KNOWLEDGE`（知识库标签）

- `create(name, type)` - 创建新标签
  - `name`: 标签名称
  - `type`: 标签类型，类型为`TagType`枚举，可选值包括`TagType.APP`（应用标签）和`TagType.KNOWLEDGE`（知识库标签）

- `delete(tag_id)` - 删除指定ID的标签
  - `tag_id`: 要删除的标签ID

## 使用示例

### 获取标签列表

```python
from dify.tag.schemas import TagType

# 初始化AdminClient和DifyTag
admin_client = AdminClient(BASE_URL, API_KEY)
dify_tag = DifyTag(admin_client)

# 获取应用标签列表
app_tags = await dify_tag.list(TagType.APP)
print(f"找到 {len(app_tags)} 个应用标签")

# 获取知识库标签列表
knowledge_tags = await dify_tag.list(TagType.KNOWLEDGE)
print(f"找到 {len(knowledge_tags)} 个知识库标签")

# 打印标签信息
for tag in app_tags:
    print(f"ID: {tag.id}")
    print(f"名称: {tag.name}")
    print(f"类型: {tag.type}")
```

### 创建标签

```python
from dify.tag.schemas import TagType

# 初始化AdminClient和DifyTag
admin_client = AdminClient(BASE_URL, API_KEY)
dify_tag = DifyTag(admin_client)

# 创建应用标签
app_tag = await dify_tag.create("测试应用标签", TagType.APP)
print(f"创建成功! 标签ID: {app_tag.id}")

# 创建知识库标签
knowledge_tag = await dify_tag.create("测试知识库标签", TagType.KNOWLEDGE)
print(f"创建成功! 标签ID: {knowledge_tag.id}")
```

### 删除标签

```python
# 初始化AdminClient和DifyTag
admin_client = AdminClient(BASE_URL, API_KEY)
dify_tag = DifyTag(admin_client)

# 删除标签
tag_id = "your_tag_id"
try:
    result = await dify_tag.delete(tag_id)
    if result:
        print("标签删除成功")
except Exception as e:
    print(f"删除标签时出错: {e}") 