#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dify SDK - 获取对话列表示例

本示例展示如何使用get_conversations方法获取Dify应用的对话列表
"""

import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv

from dify.app import DifyApp
from dify.app.conversation import ConversationListQueryPayloads
from dify.app.conversation.schemas import SortBy
from dify.http import AdminClient

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
ADMIN_API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用get_conversations方法获取对话列表"""
    # 初始化客户端
    admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)

    # 初始化DifyApp
    dify_app = DifyApp(admin_client)

    print("获取对话列表示例")
    print("-" * 30)

    app = await dify_app.find_by_id("96b8d447-293a-401c-bb7f-f9b16f9ee09b")
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

    print("\n1. 获取对话列表:")
    # 创建查询参数
    user_id = "example-user"
    payloads = ConversationListQueryPayloads(
        user=user_id,
        limit=10,
        sort_by=SortBy.UPDATED_AT_DESC,
    )

    # 获取对话列表
    print(f"\n获取用户 {user_id} 的对话列表...")
    try:
        conversations = await dify_app.conversation.get_conversations(api_key, payloads)
        
        # 打印对话列表信息
        print(f"共获取到 {len(conversations.data)} 条对话记录")
        print(f"是否有更多数据: {conversations.has_more}")
        print(f"实际返回数量: {conversations.limit}")
        
        # 打印每条对话的详细信息
        for i, conversation in enumerate(conversations.data):
            created_time = datetime.fromtimestamp(conversation.created_at).strftime('%Y-%m-%d %H:%M:%S')
            updated_time = datetime.fromtimestamp(conversation.updated_at).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"\n对话 {i+1}:")
            print(f"  ID: {conversation.id}")
            print(f"  名称: {conversation.name}")
            print(f"  状态: {conversation.status}")
            print(f"  创建时间: {created_time}")
            print(f"  更新时间: {updated_time}")
        
        # 如果有更多数据，获取下一页
        if conversations.has_more and conversations.data:
            print("\n\n2. 获取下一页数据:")
            last_id = conversations.data[-1].id
            next_page_payloads = ConversationListQueryPayloads(
                user=user_id,
                last_id=last_id,
                limit=10,
                sort_by=SortBy.UPDATED_AT_DESC,
            )
            
            print(f"获取ID为 {last_id} 之后的对话...")
            next_page = await dify_app.get_conversations(api_key, next_page_payloads)
            
            print(f"下一页获取到 {len(next_page.data)} 条对话记录")
            print(f"是否还有更多数据: {next_page.has_more}")
            
            for i, conversation in enumerate(next_page.data):
                created_time = datetime.fromtimestamp(conversation.created_at).strftime('%Y-%m-%d %H:%M:%S')
                updated_time = datetime.fromtimestamp(conversation.updated_at).strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"\n下一页对话 {i+1}:")
                print(f"  ID: {conversation.id}")
                print(f"  名称: {conversation.name}")
                print(f"  状态: {conversation.status}")
                print(f"  创建时间: {created_time}")
                print(f"  更新时间: {updated_time}")
    
    except Exception as e:
        print(f"异常类型: {type(e)}")
        print(f"获取对话列表时发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 