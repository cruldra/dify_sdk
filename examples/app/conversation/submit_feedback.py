#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dify SDK - 提交消息反馈示例

本示例展示如何使用submit_feedback方法为消息提交反馈
"""

import asyncio
import os
import traceback
from datetime import datetime

from dotenv import load_dotenv

from dify.app import DifyApp
from dify.app.conversation import MessageFeedbackPayloads, MessageListQueryPayloads, ConversationListQueryPayloads
from dify.http import AdminClient

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
ADMIN_API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用submit_feedback方法提交消息反馈"""
    # 初始化客户端
    admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)

    # 初始化DifyApp
    dify_app = DifyApp(admin_client)

    print("提交消息反馈示例")
    print("-" * 30)

    try:
        # 获取应用
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

        # 获取用户ID
        user_id = input("\n请输入用户ID (默认: example-user): ").strip() or "example-user"
        print(f"使用用户ID: {user_id}")

        # 获取对话列表
        print("\n正在获取对话列表...")
        conversations = await dify_app.conversation.find_list(
            api_key,
            ConversationListQueryPayloads(user=user_id, limit=10)
        )

        if not conversations.data:
            print("没有找到对话，请先创建对话")
            return

        # 显示对话列表
        print("\n对话列表:")
        for i, conversation in enumerate(conversations.data):
            created_time = conversation.created_at
            if created_time:
                created_time = datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')

            print(f"{i + 1}. ID: {conversation.id}, 名称: {conversation.name}, 创建时间: {created_time}")

        # 选择对话
        conversation_id = None
        while True:
            try:
                conversation_index = int(input("\n请选择对话 (输入序号): ")) - 1
                if 0 <= conversation_index < len(conversations.data):
                    conversation = conversations.data[conversation_index]
                    conversation_id = conversation.id
                    print(f"\n已选择对话: {conversation.name} (ID: {conversation_id})")
                    break
                print("无效的序号，请重新输入")
            except ValueError:
                print("请输入有效的数字")
            except KeyboardInterrupt:
                print("\n操作已取消")
                return

        # 获取消息列表
        print("\n正在获取消息列表...")
        messages = await dify_app.conversation.get_messages(
            api_key,
            MessageListQueryPayloads(
                conversation_id=conversation_id,
                user=user_id,
                first_id=None,
                limit=10,
            ),
        )

        if not messages.data:
            print("该对话没有消息，无法提交反馈")
            return

        # 显示消息列表
        print("\n消息列表:")
        for i, message in enumerate(messages.data):
            created_time = message.created_at
            if created_time:
                created_time = datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')

            query_preview = message.query[:50] + ("..." if len(message.query) > 50 else "")
            answer_preview = message.answer[:50] + ("..." if len(message.answer) > 50 else "")
            print(f"{i + 1}. [{created_time}] {query_preview}: {answer_preview}")
            print(f"   消息ID: {message.id}")

        # 选择要提交反馈的消息
        message_id = None
        while True:
            try:
                message_index = int(input("\n请选择要提交反馈的消息 (输入序号): ")) - 1
                if 0 <= message_index < len(messages.data):
                    selected_message = messages.data[message_index]
                    message_id = selected_message.id
                    print(f"\n已选择消息: {selected_message.id}")
                    print(f"消息ID: {message_id}")
                    break
                print("无效的序号，请重新输入")
            except ValueError:
                print("请输入有效的数字")
            except KeyboardInterrupt:
                print("\n操作已取消")
                return

        # 选择反馈方式
        print("\n请选择反馈方式:")
        print("1. 点赞 (like)")
        print("2. 点踩 (dislike)")

        feedback_option = None
        while True:
            try:
                option = input("请选择 (1/2): ").strip()
                if option == "1":
                    feedback_option = "like"
                    print("您选择了点赞 (like)")
                    break
                elif option == "2":
                    feedback_option = "dislike"
                    print("您选择了点踩 (dislike)")
                    break
                else:
                    print("无效的选项，请重新输入")
            except KeyboardInterrupt:
                print("\n操作已取消")
                return

        # 输入反馈内容
        print("\n请输入反馈内容 (可选，直接回车跳过):")
        feedback_content = input("> ").strip()

        # 创建反馈请求
        feedback_payloads = MessageFeedbackPayloads(
            rating=feedback_option,
            user=user_id,
            content=feedback_content if feedback_content else None,
        )

        # 确认提交
        print("\n反馈信息:")
        print(f"消息ID: {message_id}")
        print(f"反馈类型: {feedback_option}")
        if feedback_content:
            print(f"反馈内容: {feedback_content}")
        else:
            print("反馈内容: (无)")

        confirm = input("\n确认提交反馈? (y/n): ").strip().lower()
        if confirm != "y":
            print("已取消提交反馈")
            return

        # 提交反馈
        print("\n正在提交反馈...")
        result = await dify_app.conversation.submit_feedback(
            api_key,
            message_id,
            feedback_payloads,
        )

        print(f"\n反馈提交结果: {result.result}")

        # 验证反馈结果
        print("\n反馈已成功提交！")
        print(f"消息ID: {message_id}")
        print(f"反馈类型: {feedback_option}")
        if feedback_content:
            print(f"反馈内容: {feedback_content}")
        # 反馈提交成功后重新获取消息列表，然后找到这个消息，确认feedback字段是否有值
        messages = await dify_app.conversation.get_messages(
            api_key,
            MessageListQueryPayloads(
                conversation_id=conversation_id,
                user=user_id,
                # first_id=message_id,
                limit=10,
            ),
        )
        assert messages.data[0].feedback.rating == feedback_option

    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        traceback.print_exc()
        print(f"异常类型: {type(e)}")
        print(f"提交反馈时发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())
