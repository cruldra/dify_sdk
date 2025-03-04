"""
Dify SDK - 删除API密钥示例

本示例展示如何使用delete_api_key方法删除Dify应用的API密钥
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.app import DifyApp


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")
# 从环境变量获取应用ID，或者使用默认值
APP_ID = os.getenv("DIFY_APP_ID", "96b8d447-293a-401c-bb7f-f9b16f9ee09b")


async def main():
    """演示如何使用delete_api_key方法删除Dify应用的API密钥"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)

    # 初始化DifyApp
    dify_app = DifyApp(admin_client)

    print("删除API密钥示例")
    print("-" * 30)

    # 获取应用详情
    try:
        app = await dify_app.find_by_id(APP_ID)
        print(f"应用名称: {app.name}")
        print(f"应用ID: {app.id}")
        print(f"应用模式: {app.mode}")
        print()
    except Exception as e:
        print(f"获取应用详情失败: {e}")
        return

    # 获取当前API密钥列表
    print("1. 当前API密钥列表:")
    try:
        api_keys = await dify_app.get_keys(APP_ID)
        print(f"删除前一共有{len(api_keys)}个API密钥")
    except Exception as e:
        print(f"  获取API密钥列表失败: {e}")
        return

    # 删除指定的API密钥
    print(f"2. 删除API密钥 (ID: {api_keys[0].id}):")
    try:
        result = await dify_app.delete_api_key(APP_ID, api_keys[0].id)
        if result:
            print(f"  成功删除API密钥 (ID: {api_keys[0].id})")
        else:
            print(f"  删除API密钥失败")
        print()
    except Exception as e:
        print(f"  删除API密钥失败: {e}")
        return

    # 再次获取API密钥列表，确认删除成功
    print("3. 删除后的API密钥列表:")
    try:
        api_keys = await dify_app.get_keys(APP_ID)
        print(f"删除后一共有{len(api_keys)}个API密钥")
    except Exception as e:
        print(f"  获取API密钥列表失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())
