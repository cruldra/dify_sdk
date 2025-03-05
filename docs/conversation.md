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

## 获取对话列表

您可以使用`find_list`方法获取对话列表：

```python
from dify.app.conversation import ConversationListQueryPayloads

# 获取对话列表
conversations = await dify_app.conversation.find_list(
    api_key, 
    ConversationListQueryPayloads(user="user-id", limit=10)
)

# 打印对话列表
for conversation in conversations.data:
    print(f"ID: {conversation.id}, 名称: {conversation.name}")
```

## 获取消息列表

您可以使用`get_messages`方法获取特定对话的消息列表：

```python
from dify.app.conversation.schemas import MessageListQueryPayloads

# 获取消息列表
messages = await dify_app.conversation.get_messages(
    api_key,
    MessageListQueryPayloads(
        conversation_id="conversation-id",
        user="user-id",
        limit=10
    )
)

# 打印消息列表
for message in messages.data:
    print(f"ID: {message.id}, 问题: {message.query}, 回答: {message.answer}")
```

## 删除对话

您可以使用`delete`方法删除特定对话：

```python
# 删除对话
result = await dify_app.conversation.delete(
    api_key,
    conversation_id="conversation-id",
    user_id="user-id"
)

# 检查删除结果
if result.result == "success":
    print("对话删除成功")
else:
    print("对话删除失败")
```

## 重命名对话

您可以使用`rename`方法重命名特定对话：

```python
from dify.app.conversation.schemas import ConversationRenamePayloads

# 手动指定新名称
rename_payloads = ConversationRenamePayloads(
    name="新对话名称",
    auto_generate=False,
    user="user-id"
)

# 重命名对话
renamed_conversation = await dify_app.conversation.rename(
    api_key,
    conversation_id="conversation-id",
    payloads=rename_payloads
)

print(f"对话已重命名为: {renamed_conversation.name}")

# 自动生成对话名称
auto_rename_payloads = ConversationRenamePayloads(
    auto_generate=True,
    user="user-id"
)

# 自动重命名对话
auto_renamed_conversation = await dify_app.conversation.rename(
    api_key,
    conversation_id="conversation-id",
    payloads=auto_rename_payloads
)

print(f"对话已自动重命名为: {auto_renamed_conversation.name}")
```

## 完整示例

完整示例请参考以下文件：

- 获取对话列表：[examples/app/conversation/find_list.py](../examples/app/conversation/find_list.py)
- 获取消息列表：[examples/app/conversation/get_messages.py](../examples/app/conversation/get_messages.py)
- 删除对话：[examples/app/conversation/delete_conversation.py](../examples/app/conversation/delete_conversation.py)
- 重命名对话：[examples/app/conversation/rename_conversation.py](../examples/app/conversation/rename_conversation.py) 