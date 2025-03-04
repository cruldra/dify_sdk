"""
Dify SDK - 聊天功能示例

本示例展示如何使用chat方法与Dify应用进行对话交互
"""

import asyncio
import os

from dotenv import load_dotenv

from dify.app import DifyApp
from dify.app.schemas import (
    ChatMessageEvent,
    ChatPayloads,
    ErrorEvent,
    MessageEndEvent,
)
from dify.http import AdminClient

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
ADMIN_API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用chat方法与Dify应用进行对话交互"""
    # 初始化客户端
    admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)

    # 初始化DifyApp
    dify_app = DifyApp(admin_client)

    print("聊天功能示例")
    print("-" * 30)

    # 首先获取应用列表，以便获取一个有效的应用ID
    app_list = await dify_app.find_list(limit=1, name="中国法律助手")

    if not app_list.data:
        print("未找到任何应用，请确保您的账户中有创建的应用")
        return

    # 获取第一个应用
    app = app_list.data[0]
    print(f"使用应用: {app.name} (ID: {app.id}, 模式: {app.mode})")

    print("\n1. 发起聊天对话:")
    # 创建聊天请求配置
    payloads = ChatPayloads(
        query="你好，请介绍一下自己",
        user="example-user",
        response_mode="streaming",
    )

    # 发送聊天请求
    print("\n开始聊天...")
    answer_text = ""
    conversation_id = None
    app_key = await dify_app.create_api_key(app.id)
    async for event in dify_app.chat(app_key.token, payloads):
        print("事件类型:", event.event)
        if isinstance(event, ChatMessageEvent):
            print(f"ai响应: {event.answer}", end="", flush=True)
        if isinstance(event, MessageEndEvent):
            print("\n\n对话结束")
            break
        if isinstance(event, ErrorEvent):
            print(f"\n错误: {event.message}", end="", flush=True)
            break


if __name__ == "__main__":
    asyncio.run(main())
