#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dify SDK - 获取消息列表示例

本示例展示如何使用get_messages方法获取Dify会话的消息列表
"""

import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv

from dify.app import DifyApp
from dify.app.conversation import ConversationListQueryPayloads
from dify.app.conversation.schemas import MessageListQueryPayloads
from dify.http import AdminClient

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
ADMIN_API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用get_messages方法获取消息列表"""
    # 初始化客户端
    admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)

    # 初始化DifyApp
    dify_app = DifyApp(admin_client)

    print("获取消息列表示例")
    print("-" * 30)

    # 获取应用
    try:
        # 这里可以替换为您的应用ID
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

        # 获取对话列表，以便获取一个对话ID
        user_id = "example-user"
        print(f"\n获取用户 {user_id} 的对话列表...")
        conversations = await dify_app.conversation.find_list(
            api_key, 
            ConversationListQueryPayloads(user=user_id, limit=1)
        )
        
        if not conversations.data:
            print(f"用户 {user_id} 没有对话记录，请先创建对话")
            return
            
        conversation_id = conversations.data[0].id
        print(f"使用对话ID: {conversation_id}")

        print("\n1. 获取消息列表:")
        # 创建查询参数
        payloads = MessageListQueryPayloads(
            conversation_id=conversation_id,
            user=user_id,
            limit=10,
        )

        # 获取消息列表
        messages = await dify_app.conversation.get_messages(api_key, payloads)
        
        # 打印消息列表信息
        print(f"共获取到 {len(messages.data)} 条消息记录")
        print(f"是否有更多数据: {messages.has_more}")
        print(f"实际返回数量: {messages.limit}")
        
        # 打印每条消息的详细信息
        for i, message in enumerate(messages.data):
            created_time = message.created_time or (
                datetime.fromtimestamp(message.created_at).strftime('%Y-%m-%d %H:%M:%S') 
                if message.created_at else "未知时间"
            )
            
            print(f"\n消息 {i+1}:")
            print(f"  ID: {message.id}")
            print(f"  会话ID: {message.conversation_id}")
            print(f"  用户问题: {message.query}")
            print(f"  AI回答: {message.answer[:100]}..." if message.answer and len(message.answer) > 100 else f"  AI回答: {message.answer}")
            print(f"  创建时间: {created_time}")
            
            # 打印消息文件信息
            if message.message_files:
                print(f"  附件数量: {len(message.message_files)}")
                for j, file in enumerate(message.message_files):
                    print(f"    文件 {j+1}: {file.filename} ({file.mime_type})")
            
            # 打印检索资源信息
            if message.retriever_resources:
                print(f"  检索资源数量: {len(message.retriever_resources)}")
                for j, resource in enumerate(message.retriever_resources):
                    print(f"    资源 {j+1}: {resource.source}")
        
        # 如果有更多数据，获取下一页
        if messages.has_more and messages.data:
            print("\n\n2. 获取下一页数据:")
            first_id = messages.data[-1].id
            next_page_payloads = MessageListQueryPayloads(
                conversation_id=conversation_id,
                user=user_id,
                first_id=first_id,
                limit=10,
            )
            
            print(f"获取ID为 {first_id} 之后的消息...")
            next_page = await dify_app.conversation.get_messages(api_key, next_page_payloads)
            
            print(f"下一页获取到 {len(next_page.data)} 条消息记录")
            print(f"是否还有更多数据: {next_page.has_more}")
            
            for i, message in enumerate(next_page.data):
                created_time = message.created_time or (
                    datetime.fromtimestamp(message.created_at).strftime('%Y-%m-%d %H:%M:%S') 
                    if message.created_at else "未知时间"
                )
                
                print(f"\n下一页消息 {i+1}:")
                print(f"  ID: {message.id}")
                print(f"  用户问题: {message.query}")
                print(f"  AI回答: {message.answer[:50]}..." if message.answer and len(message.answer) > 50 else f"  AI回答: {message.answer}")
                print(f"  创建时间: {created_time}")
    
    except Exception as e:
        print(f"异常类型: {type(e)}")
        print(f"获取消息列表时发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 