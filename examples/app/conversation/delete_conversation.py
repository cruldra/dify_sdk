#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dify SDK - 删除对话示例

本示例展示如何使用delete方法删除Dify会话
"""

import asyncio
import os
import traceback
from datetime import datetime

from dotenv import load_dotenv

from dify.app import DifyApp
from dify.app.conversation import ConversationListQueryPayloads
from dify.http import AdminClient

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
ADMIN_API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用delete方法删除对话"""
    # 初始化客户端
    admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)

    # 初始化DifyApp
    dify_app = DifyApp(admin_client)

    print("删除对话示例")
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

        # 获取对话列表
        user_id = "example-user"
        print(f"\n获取用户 {user_id} 的对话列表...")
        conversations = await dify_app.conversation.find_list(
            api_key, 
            ConversationListQueryPayloads(user=user_id, limit=5)
        )
        
        if not conversations.data:
            print(f"用户 {user_id} 没有对话记录，无法执行删除操作")
            return
            
        # 打印对话列表
        print(f"找到 {len(conversations.data)} 个对话:")
        for i, conversation in enumerate(conversations.data):
            created_time = conversation.created_at
            if created_time:
                created_time = datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"{i+1}. ID: {conversation.id}, 名称: {conversation.name}, 创建时间: {created_time}")
        
        # 选择要删除的对话
        if len(conversations.data) > 0:
            # 这里选择第一个对话进行删除，实际应用中可以让用户选择
            conversation_to_delete = conversations.data[0]
            conversation_id = conversation_to_delete.id
            
            print(f"\n准备删除对话: {conversation_to_delete.name} (ID: {conversation_id})")
            
            # 确认删除
            confirm = input("确认删除此对话? (y/n): ")
            if confirm.lower() != 'y':
                print("已取消删除操作")
                return
                
            # 执行删除操作
            print(f"正在删除对话 {conversation_id}...")
            result = await dify_app.conversation.delete(api_key, conversation_id, user_id)
            
            print(f"删除结果: {result.result}")
            
            # 验证删除结果
            print("\n验证删除结果...")
            updated_conversations = await dify_app.conversation.find_list(
                api_key, 
                ConversationListQueryPayloads(user=user_id, limit=5)
            )
            
            # 检查被删除的对话是否还存在
            deleted = True
            for conv in updated_conversations.data:
                if conv.id == conversation_id:
                    deleted = False
                    break
                    
            if deleted:
                print(f"对话 {conversation_id} 已成功删除!")
            else:
                print(f"对话 {conversation_id} 删除失败，仍然存在于列表中")
    
    except Exception as e:
        traceback.print_exc()
        print(f"异常类型: {type(e)}")
        print(f"删除对话时发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 