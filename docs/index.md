# Dify SDK 文档

Dify SDK 是一个用于与 Dify API 交互的 Python 库。

## 安装

使用 uv 安装:

```bash
uv pip install dify-sdk
```

或者使用 pip 安装:

```bash
pip install dify-sdk
```

## 基本用法

```python
from dify import Dify

# 初始化客户端
dify = Dify(api_key="your_api_key")

# 异步使用示例
import asyncio

async def main():
    # 获取应用列表
    apps = await dify.app.find_list()
    print(f"找到 {len(apps.data)} 个应用")

# 运行异步函数
asyncio.run(main())
```

## 功能

### 应用管理

- `find_list()`: 获取应用列表
- `find_by_id(app_id)`: 获取应用详情
- `get_keys(app_id)`: 获取应用的API密钥列表
- `create_api_key(app_id)`: 创建API密钥
- `delete_api_key(app_id, key_id)`: 删除API密钥

### 对话功能

- `chat(key, payloads)`: 与应用进行对话
- `completion(api_key, payloads)`: 使用应用进行补全
- `run(api_key, payloads)`: 运行工作流
- `fetch_conversations(api_key, payloads)`: 获取对话列表
- `get_messages(api_key, payloads)`: 获取消息列表

## 获取对话列表

使用 `fetch_conversations` 方法可以获取对话列表：

```python
from dify import Dify
from dify.app.schemas import ConversationListQueryPayloads, SortBy

async def get_conversations():
    # 初始化客户端
    dify = Dify(api_key="your_api_key")
    
    # 获取应用列表
    app = await dify.app.find_list(limit=1)
    if not app.data:
        return
    
    # 获取API密钥
    app_id = app.data[0].id
    keys = await dify.app.get_keys(app_id)
    if not keys:
        return
    
    # 创建查询参数
    query_params = ConversationListQueryPayloads(
        user="user_id",
        limit=20,
        sort_by=SortBy.UPDATED_AT_DESC,
    )
    
    # 获取对话列表
    conversations = await dify.app.fetch_conversations(keys[0], query_params)
    
    # 处理结果
    for conversation in conversations.data:
        print(f"对话ID: {conversation.id}, 名称: {conversation.name}")
    
    # 分页处理
    if conversations.has_more:
        last_id = conversations.data[-1].id
        # 获取下一页
        next_page_params = ConversationListQueryPayloads(
            user="user_id",
            last_id=last_id,
            limit=20,
            sort_by=SortBy.UPDATED_AT_DESC,
        )
        next_page = await dify.app.fetch_conversations(keys[0], next_page_params)
```

### 参数说明

`fetch_conversations` 方法接受以下参数：

- `api_key`: API密钥对象
- `payloads`: 查询参数配置，类型为 `ConversationListQueryPayloads`

`ConversationListQueryPayloads` 包含以下字段：

- `user`: 用户标识，需保证在应用内唯一
- `last_id`: (可选) 当前页最后一条记录的ID，用于分页
- `limit`: (可选) 一次请求返回多少条记录，默认20条，最大100条，最小1条
- `sort_by`: (可选) 排序字段，可选值：
  - `SortBy.CREATED_AT_ASC`: 按创建时间升序
  - `SortBy.CREATED_AT_DESC`: 按创建时间降序
  - `SortBy.UPDATED_AT_ASC`: 按更新时间升序
  - `SortBy.UPDATED_AT_DESC`: 按更新时间降序，默认值

### 返回值

方法返回 `ConversationList` 对象，包含以下字段：

- `data`: 对话列表，每个元素为 `Conversation` 对象
- `has_more`: 是否有更多数据
- `limit`: 实际返回数量

`Conversation` 对象包含以下字段：

- `id`: 对话ID
- `name`: 对话名称
- `inputs`: 用户输入参数
- `status`: 对话状态
- `introduction`: 开场白
- `created_at`: 创建时间戳
- `updated_at`: 更新时间戳

## 获取消息列表

使用 `get_messages` 方法可以获取特定对话的消息列表：

```python
from dify import Dify
from dify.app.conversation.schemas import MessageListQueryPayloads
from dify.schemas import ApiKey

async def get_messages():
    # 初始化客户端
    dify = Dify(base_url="https://api.dify.ai")
    
    # 创建API密钥对象
    api_key = ApiKey(token="your_api_key")
    
    # 创建查询参数
    query_params = MessageListQueryPayloads(
        conversation_id="conversation_id",  # 对话ID
        user="user_id",                     # 用户ID
        first_id=None,                      # 当前页第一条聊天记录的ID，用于分页
        limit=20                            # 返回消息数量
    )
    
    # 获取消息列表
    message_list = await dify.conversation.get_messages(
        api_key=api_key,
        payloads=query_params
    )
    
    # 处理结果
    print(f"获取到 {len(message_list.data)} 条消息")
    print(f"是否有更多消息: {message_list.has_more}")
    
    # 遍历消息
    for message in message_list.data:
        print(f"消息ID: {message.id}")
        print(f"用户问题: {message.query}")
        print(f"AI回答: {message.answer}")
        print(f"创建时间: {message.created_time}")
        
    # 分页获取更多消息
    if message_list.has_more and message_list.data:
        # 使用最后一条消息的ID作为下一页的first_id
        last_message_id = message_list.data[-1].id
        
        # 创建新的查询参数
        next_page_params = MessageListQueryPayloads(
            conversation_id="conversation_id",
            user="user_id",
            first_id=last_message_id,
            limit=20
        )
        
        # 获取下一页消息
        next_page = await dify.conversation.get_messages(
            api_key=api_key,
            payloads=next_page_params
        )
```

### 参数说明

`get_messages` 方法接受以下参数：

- `api_key`: API密钥对象
- `payloads`: 查询参数配置，类型为 `MessageListQueryPayloads`

`MessageListQueryPayloads` 包含以下字段：

- `conversation_id`: 对话ID
- `user`: 用户ID
- `first_id`: (可选) 当前页第一条聊天记录的ID，用于分页
- `limit`: (可选) 返回消息数量，默认20条，最大100条，最小1条

### 返回值

方法返回 `MessageList` 对象，包含以下字段：

- `data`: 消息列表，每个元素为 `Message` 对象
- `has_more`: 是否有更多数据
- `limit`: 实际返回数量

`Message` 对象包含以下字段：

- `id`: 消息ID
- `query`: 用户问题
- `answer`: AI回答
- `created_time`: 创建时间
