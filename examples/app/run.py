"""
Dify SDK - 工作流运行示例

本示例展示如何使用run方法运行Dify工作流应用
"""

import asyncio
import os

from dotenv import load_dotenv

from dify.app import DifyApp
from dify.app.schemas import (
    ConversationEventType,
    ChatMessageEvent,
    ErrorEvent,
    MessageEndEvent,
    RunWorkflowPayloads,
)
from dify.http import AdminClient

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
ADMIN_API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用run方法运行Dify工作流应用"""
    # 初始化客户端
    admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)

    # 初始化DifyApp
    dify_app = DifyApp(admin_client)

    print("工作流运行示例")
    print("-" * 30)

    # 首先获取应用列表，以便获取一个工作流应用
    app = await dify_app.find_by_id("5e9cc886-ab40-455f-9bd2-d19d4dedfc02")

    print(f"使用工作流应用: {app.name} (ID: {app.id}, 模式: {app.mode})")

    print("\n1. 运行工作流:")
    # 创建工作流请求配置
    payloads = RunWorkflowPayloads(
        inputs={"theme": "发财了","count":"五言"},
        user="example-user",
        response_mode="streaming",
    )

    # 获取应用API密钥
    api_keys = await dify_app.get_keys(app.id)
    if not api_keys:
        print(f"应用 {app.name} 没有API密钥，请先创建API密钥")
        return
    
    api_key = api_keys[0]
    print(f"使用API密钥: {api_key.id}")

    # 运行工作流
    print("\n开始运行工作流...")
    async for event in dify_app.run(api_key, payloads):
        print("事件类型:", event.event)
        
        print(f"事件内容:{event.model_dump_json(indent=4)}")


if __name__ == "__main__":
    asyncio.run(main()) 