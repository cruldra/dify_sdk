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

## 快速开始

```python
import asyncio
from dify import DifyClient

async def main():
    # 初始化客户端
    client = DifyClient("https://api.dify.ai/v1", "your-api-key")
    
    # 获取应用列表
    apps = await client.app.find_list()
    print(f"应用总数: {apps.total}")
    
    # 创建新应用
    new_app = await client.app.create(
        name="我的聊天应用",
        mode="chat",
        description="这是一个简单的聊天应用"
    )
    print(f"创建应用成功: {new_app.name} (ID: {new_app.id})")

if __name__ == "__main__":
    asyncio.run(main())
```

## 应用管理

### 创建应用

使用 `create` 方法创建新应用:

```python
app = await client.app.create(
    name="我的聊天应用",
    mode="chat",  # 可选值: chat, agent-chat, workflow, completion
    description="这是一个简单的聊天应用",
    icon_type="emoji",  # 默认为 emoji
    icon="🤖",  # 默认为 🤖
    icon_background="#FFEAD5"  # 默认为 #FFEAD5
)
```

### 获取应用列表

使用 `find_list` 方法获取应用列表:

```python
apps = await client.app.find_list(
    page=1,
    limit=10,
    mode="chat",  # 可选，按应用模式过滤
    name="",  # 可选，按名称过滤
    is_created_by_me=True  # 可选，只返回由我创建的应用
)
```

### 获取应用详情

使用 `find_by_id` 方法获取应用详情:

```python
app = await client.app.find_by_id("app-id")
```

### 获取应用API密钥

使用 `get_keys` 方法获取应用的API密钥:

```python
keys = await client.app.get_keys("app-id")
```

### 创建API密钥

使用 `create_api_key` 方法为应用创建新的API密钥:

```python
key = await client.app.create_api_key("app-id")
```

### 删除API密钥

使用 `delete_api_key` 方法删除应用的API密钥:

```python
result = await client.app.delete_api_key("app-id", "key-id")
```

## 对话

### 聊天

使用 `chat` 方法与应用进行对话:

```python
async for event in client.app.chat(
    "api-key",
    {
        "query": "你好",
        "user": "user-id",
        "response_mode": "streaming"
    }
):
    print(event)
```

### 补全

使用 `completion` 方法获取补全结果:

```python
async for event in client.app.completion(
    "api-key",
    {
        "inputs": {},
        "user": "user-id",
        "response_mode": "streaming"
    }
):
    print(event)
```

### 运行工作流

使用 `run` 方法运行工作流:

```python
async for event in client.app.run(
    "api-key",
    {
        "inputs": {},
        "user": "user-id",
        "response_mode": "streaming"
    }
):
    print(event)
```

### 获取应用参数

使用 `get_parameters` 方法获取应用参数:

```python
parameters = await client.app.get_parameters("api-key")
```

### 停止消息生成

使用 `stop_message` 方法停止消息生成:

```python
result = await client.app.stop_message("api-key", "task-id", "user-id")
```

## 更多示例

查看 `examples` 目录获取更多使用示例。

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
