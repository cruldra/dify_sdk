# Dify SDK - 对话管理

本文档介绍如何使用Dify SDK管理对话。

## 初始化

首先，您需要初始化`DifyApp`对象：

```python
from dify.app import DifyApp
from dify.http import AdminClient

# 初始化客户端
admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)

# 初始化DifyApp
dify_app = DifyApp(admin_client)
```

## 对话管理

Dify SDK提供了对话管理功能，包括获取对话列表、获取消息列表、删除对话、重命名对话和提交消息反馈等操作。

### 获取对话列表

使用`find_list`方法获取对话列表：

```python
from dify import Dify
from dify.app.conversation import ConversationListQueryPayloads

# 初始化Dify客户端
dify = Dify(base_url="https://api.dify.ai/v1")

# 获取API密钥
api_key = await dify.application.get_api_key(admin_api_key, app_id)

# 创建查询参数
payloads = ConversationListQueryPayloads(
    first_id=None,  # 第一个对话ID，用于分页
    limit=10,       # 每页数量
    user="user_123" # 用户ID
)

# 获取对话列表
conversations = await dify.conversation.find_list(api_key, payloads)

# 打印对话列表
for conversation in conversations.data:
    print(f"对话ID: {conversation.id}, 名称: {conversation.name}")
```

### 获取消息列表

使用`get_messages`方法获取特定对话的消息列表：

```python
from dify import Dify
from dify.app.conversation import MessageListQueryPayloads

# 初始化Dify客户端
dify = Dify(base_url="https://api.dify.ai/v1")

# 获取API密钥
api_key = await dify.application.get_api_key(admin_api_key, app_id)

# 创建查询参数
payloads = MessageListQueryPayloads(
    conversation_id="conversation_123", # 对话ID
    first_id=None,                      # 第一个消息ID，用于分页
    limit=20                            # 每页数量
)

# 获取消息列表
messages = await dify.conversation.get_messages(api_key, payloads)

# 打印消息列表
for message in messages.data:
    print(f"消息ID: {message.id}, 角色: {message.role}, 内容: {message.content[:50]}...")
```

### 删除对话

使用`delete`方法删除特定对话：

```python
from dify import Dify

# 初始化Dify客户端
dify = Dify(base_url="https://api.dify.ai/v1")

# 获取API密钥
api_key = await dify.application.get_api_key(admin_api_key, app_id)

# 删除对话
result = await dify.conversation.delete(
    api_key=api_key,
    conversation_id="conversation_123", # 对话ID
    user_id="user_123"                  # 用户ID
)

# 打印结果
print(f"删除结果: {result.result}")
```

### 重命名对话

使用`rename`方法重命名特定对话：

```python
from dify import Dify
from dify.app.conversation import ConversationRenamePayloads

# 初始化Dify客户端
dify = Dify(base_url="https://api.dify.ai/v1")

# 获取API密钥
api_key = await dify.application.get_api_key(admin_api_key, app_id)

# 方法1：手动指定新名称
payloads = ConversationRenamePayloads(
    name="新对话名称",
    auto_generate=False,
    user="user_123"  # 用户ID
)

# 方法2：自动生成名称
# payloads = ConversationRenamePayloads(
#     auto_generate=True,
#     user="user_123"  # 用户ID
# )

# 重命名对话
conversation = await dify.conversation.rename(
    api_key=api_key,
    conversation_id="conversation_123", # 对话ID
    payloads=payloads
)

# 打印结果
print(f"重命名后的对话: {conversation.name}")
```

### 提交消息反馈

使用`submit_feedback`方法提交对特定消息的反馈：

```python
from dify import Dify
from dify.app.conversation import MessageFeedbackPayloads

# 初始化Dify客户端
dify = Dify(base_url="https://api.dify.ai/v1")

# 获取API密钥
api_key = await dify.application.get_api_key(admin_api_key, app_id)

# 创建反馈参数
payloads = MessageFeedbackPayloads(
    rating="like",                    # 评分，可选值: "like" 或 "dislike"
    user="user_123",                  # 用户ID
    content="这是一个很有帮助的回答！"  # 可选的反馈内容
)

# 提交反馈
result = await dify.conversation.submit_feedback(
    api_key=api_key,
    message_id="message_123",  # 消息ID
    payloads=payloads
)

# 打印结果
print(f"反馈提交结果: {result.result}")
```

## 完整示例

- [获取对话列表示例](../examples/app/conversation/find_list.py)
- [获取消息列表示例](../examples/app/conversation/get_messages.py)
- [删除对话示例](../examples/app/conversation/delete_conversation.py)
- [重命名对话示例](../examples/app/conversation/rename_conversation.py)
- [提交消息反馈示例](../examples/app/conversation/submit_feedback.py) 