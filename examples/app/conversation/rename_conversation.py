#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dify SDK - 重命名对话示例

本示例展示如何使用rename方法重命名Dify会话
"""

import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv

from dify.app import DifyApp
from dify.app.conversation import ConversationListQueryPayloads
from dify.app.conversation.schemas import ConversationRenamePayloads
from dify.http import AdminClient

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
ADMIN_API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用rename方法重命名对话"""
    # 初始化客户端
    admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)

    # 初始化DifyApp
    dify_app = DifyApp(admin_client)

    print("重命名对话示例")
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
            print(f"用户 {user_id} 没有对话记录，无法执行重命名操作")
            return
            
        # 打印对话列表
        print(f"找到 {len(conversations.data)} 个对话:")
        for i, conversation in enumerate(conversations.data):
            created_time = conversation.created_at
            if created_time:
                created_time = datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"{i+1}. ID: {conversation.id}, 名称: {conversation.name}, 创建时间: {created_time}")
        
        # 选择要重命名的对话
        if len(conversations.data) > 0:
            # 让用户选择要重命名的对话
            while True:
                try:
                    choice = input("\n请选择要重命名的对话编号 (1-{}): ".format(len(conversations.data)))
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(conversations.data):
                        break
                    else:
                        print(f"请输入1-{len(conversations.data)}之间的数字")
                except ValueError:
                    print("请输入有效的数字")
            
            conversation_to_rename = conversations.data[choice_idx]
            conversation_id = conversation_to_rename.id
            
            print(f"\n已选择对话: {conversation_to_rename.name} (ID: {conversation_id})")
            
            # 重命名选项菜单
            print("\n重命名选项:")
            print("1. 手动输入新名称")
            print("2. 自动生成名称")
            
            rename_option = input("请选择重命名方式 (1/2): ")
            
            if rename_option == "1":
                # 手动输入新名称
                new_name = input("请输入新的对话名称: ")
                if not new_name.strip():
                    print("名称不能为空，使用默认名称")
                    new_name = f"重命名测试-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                print(f"将对话重命名为: {new_name}")
                
                # 创建重命名请求参数
                rename_payloads = ConversationRenamePayloads(
                    name=new_name,
                    auto_generate=False,
                    user=user_id
                )
                
                # 执行重命名操作
                print("正在重命名对话...")
                renamed_conversation = await dify_app.conversation.rename(
                    api_key, 
                    conversation_id, 
                    rename_payloads
                )
                
                print(f"重命名结果: ID: {renamed_conversation.id}, 新名称: {renamed_conversation.name}")
                
            elif rename_option == "2":
                # 自动生成名称
                print("尝试自动生成对话名称...")
                
                # 创建自动生成名称的请求参数
                auto_rename_payloads = ConversationRenamePayloads(
                    auto_generate=True,
                    user=user_id
                )
                
                # 执行自动重命名操作
                print("正在自动生成对话名称...")
                auto_renamed_conversation = await dify_app.conversation.rename(
                    api_key, 
                    conversation_id, 
                    auto_rename_payloads
                )
                
                print(f"自动重命名结果: ID: {auto_renamed_conversation.id}, 新名称: {auto_renamed_conversation.name}")
            
            else:
                print("无效的选项，操作取消")
                return
            
            # 验证重命名结果
            print("\n验证重命名结果...")
            updated_conversations = await dify_app.conversation.find_list(
                api_key, 
                ConversationListQueryPayloads(user=user_id, limit=5)
            )
            
            # 查找被重命名的对话
            for conv in updated_conversations.data:
                if conv.id == conversation_id:
                    print(f"对话 {conversation_id} 当前名称: {conv.name}")
                    break
    
    except Exception as e:
        print(f"异常类型: {type(e)}")
        print(f"重命名对话时发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 