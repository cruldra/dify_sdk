#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dify SDK - 获取应用参数示例

本示例展示如何使用get_parameters方法获取应用参数配置
"""

import asyncio
import os

from dotenv import load_dotenv

from dify.app import DifyApp
from dify.http import AdminClient

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
ADMIN_API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用get_parameters方法获取应用参数配置"""
    # 初始化客户端
    admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)

    # 初始化DifyApp
    dify_app = DifyApp(admin_client)

    print("获取应用参数示例")
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

        # 获取应用参数配置
        print("\n正在获取应用参数配置...")
        parameters = await dify_app.get_parameters(api_key)

        # 打印应用参数配置
        print("\n应用参数配置:")
        print(f"开场白: {parameters.opening_statement}")

        # 打印推荐问题
        if parameters.suggested_questions:
            print("\n开场推荐问题:")
            for i, question in enumerate(parameters.suggested_questions):
                print(f"{i + 1}. {question}")
        else:
            print("\n没有设置开场推荐问题")

        # 打印回答后推荐问题配置
        print("\n回答后推荐问题配置:")
        print(f"启用状态: {parameters.suggested_questions_after_answer.enabled}")

        # 打印语音转文本配置
        print("\n语音转文本配置:")
        print(f"启用状态: {parameters.speech_to_text.enabled}")

        # 打印引用和归属配置
        print("\n引用和归属配置:")
        print(f"启用状态: {parameters.retriever_resource.enabled}")

        # 打印标记回复配置
        print("\n标记回复配置:")
        print(f"启用状态: {parameters.annotation_reply.enabled}")

        # 打印用户输入项
        if parameters.user_input_form:
            print("\n用户输入项:")
            for i, input_item in enumerate(parameters.user_input_form):
                print(f"{i + 1}. 变量名: {input_item.variable}, 标签: {input_item.label}, 类型: {input_item.type}")
        else:
            print("\n没有设置用户输入项")

        # 打印文件上传配置
        print("\n文件上传配置:")
        print(f"启用状态: {parameters.file_upload.image.enabled}")
        if parameters.file_upload.image.enabled:
            print(f"允许的文件类型: {parameters.file_upload.image.number_limits}")
            print(f"传递方式: {parameters.file_upload.image.transfer_methods}")
    except Exception as e:
        print(f"异常类型: {type(e)}")
        print(f"获取应用参数时发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())
