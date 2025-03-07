#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dify SDK - 创建应用示例

本示例展示如何使用create方法创建Dify应用
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.app import DifyApp
from dify.app.schemas import AppMode


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用create方法创建Dify应用"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyApp
    dify_app = DifyApp(admin_client)
    
    print("创建应用示例")
    print("-" * 30)
    
    print("1. 创建聊天应用:")
    chat_app = await dify_app.create(
        name="我的聊天应用",
        mode=AppMode.CHAT,
        description="这是一个简单的聊天应用示例",
        icon="💬",
        icon_background="#E7F8FF"
    )
    print(f"  应用名称: {chat_app.name}")
    print(f"  应用ID: {chat_app.id}")
    print(f"  应用模式: {chat_app.mode}")
    print(f"  应用描述: {chat_app.description}")
    print()
    
    print("2. 创建工作流应用:")
    workflow_app = await dify_app.create(
        name="我的工作流应用",
        mode=AppMode.WORKFLOW,
        description="这是一个简单的工作流应用示例",
        icon="🔄",
        icon_background="#F0FFF4"
    )
    print(f"  应用名称: {workflow_app.name}")
    print(f"  应用ID: {workflow_app.id}")
    print(f"  应用模式: {workflow_app.mode}")
    print(f"  应用描述: {workflow_app.description}")
    print()
    
    print("3. 创建补全应用:")
    completion_app = await dify_app.create(
        name="我的补全应用",
        mode=AppMode.COMPLETION,
        description="这是一个简单的补全应用示例",
        icon="✏️",
        icon_background="#FFF5F7"
    )
    print(f"  应用名称: {completion_app.name}")
    print(f"  应用ID: {completion_app.id}")
    print(f"  应用模式: {completion_app.mode}")
    print(f"  应用描述: {completion_app.description}")
    print()
    
    print("4. 创建代理聊天应用:")
    agent_chat_app = await dify_app.create(
        name="我的代理聊天应用",
        mode=AppMode.AGENT_CHAT,
        description="这是一个简单的代理聊天应用示例",
        icon="🤖",
        icon_background="#F0E7FF"
    )
    print(f"  应用名称: {agent_chat_app.name}")
    print(f"  应用ID: {agent_chat_app.id}")
    print(f"  应用模式: {agent_chat_app.mode}")
    print(f"  应用描述: {agent_chat_app.description}")
    print()
    
    print("5. 获取应用列表:")
    app_list = await dify_app.find_list(page=1, limit=10)
    print(f"  应用总数: {app_list.total}")
    print("  应用列表:")
    for app in app_list.data:
        print(f"  - {app.name} (ID: {app.id}, 模式: {app.mode})")


if __name__ == "__main__":
    asyncio.run(main()) 