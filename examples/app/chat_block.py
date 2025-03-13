"""
Dify SDK - 聊天功能示例

本示例展示如何使用chat方法与Dify应用进行对话交互
"""

import asyncio
import os
import traceback

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
    """演示如何使用chat_block方法与Dify应用进行对话交互"""
    # 初始化客户端
    admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)

    # 初始化DifyApp
    dify_app = DifyApp(admin_client)

    print("聊天功能示例")
    
    # 首先获取应用列表，以便获取一个有效的应用ID
    app_list = await dify_app.find_list(limit=1, name="中国法律助手")

    if not app_list.data:
        print("未找到任何应用，请确保您的账户中有创建的应用")
        return
    
    # 获取应用的API密钥
    api_keys = await dify_app.get_keys(app_list.data[0].id)
    if not api_keys:
        print("未找到任何API密钥，请确保您的应用有API密钥")
        return
    
    # 获取第一个API密钥
    app_key = api_keys[0]
    print(f"使用应用: {app_list.data[0].name} (ID: {app_list.data[0].id}, 模式: {app_list.data[0].mode})")

    # 创建聊天请求配置
    payloads = ChatPayloads(
        query="跟我说:'你好!'",
        user="example-user",
        response_mode="blocking",
    )

    # 发送聊天请求
    print("\n开始聊天...")
    try:
        response = await dify_app.chat_block(app_key, payloads)
        print(f"AI响应: {response.answer}")
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

