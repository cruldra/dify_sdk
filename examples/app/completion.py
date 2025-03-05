"""
Dify SDK - 补全功能示例

本示例展示如何使用completion方法与Dify应用进行补全交互
"""

import asyncio
import os

from dotenv import load_dotenv

from dify.app import DifyApp
from dify.app.schemas import (
    ChatMessageEvent,
    ErrorEvent,
    MessageEndEvent, RunWorkflowPayloads,
)
from dify.http import AdminClient

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
ADMIN_API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用completion方法与Dify应用进行补全交互"""
    # 初始化客户端
    admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)

    # 初始化DifyApp
    dify_app = DifyApp(admin_client)

    print("补全功能示例")
    print("-" * 30)

    # 首先获取应用列表，以便获取一个有效的应用ID
    app = await dify_app.find_by_id("680289bc-1483-4ac8-8ec5-161828a87a8b")

    print(f"使用应用: {app.name} (ID: {app.id}, 模式: {app.mode})")

    # 获取应用的API密钥
    api_keys = await dify_app.get_keys(app.id)
    if not api_keys:
        print(f"应用 {app.name} 没有API密钥，正在创建...")
        api_key = await dify_app.create_api_key(app.id)
        print(f"已创建API密钥: {api_key.token}")
    else:
        api_key = api_keys[0]
        print(f"使用现有API密钥: {api_key.id}")

    print("\n1. 发起补全请求:")
    # 创建补全请求配置
    payloads = RunWorkflowPayloads(
        inputs={
            "query": "我是你大爹"
        },
        user="example-user",
        response_mode="streaming",
    )

    # 发送补全请求
    print("\n开始补全...")
    answer_text = ""
    async for event in dify_app.completion(api_key, payloads):
        print("事件类型:", event.event)
        if isinstance(event, ChatMessageEvent):
            print(f"补全内容: {event.answer}", flush=True)
            answer_text += event.answer
        if isinstance(event, MessageEndEvent):
            print("\n\n补全结束")
            break
        if isinstance(event, ErrorEvent):
            print(f"\n错误: {event.message}", flush=True)
            break

    print("\n\n完整的补全结果:")
    print(answer_text)


if __name__ == "__main__":
    asyncio.run(main())
