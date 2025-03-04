"""
Dify SDK - 创建API密钥示例

本示例展示如何使用create_api_key方法为Dify应用创建API密钥
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
    """演示如何使用create_api_key方法为Dify应用创建API密钥"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyApp
    dify_app = DifyApp(admin_client)
    
    print("创建API密钥示例")
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
    
    # 创建只读API密钥
    print("1. 创建密钥:")
    try:
        read_api_key = await dify_app.create_api_key(
            app_id=APP_ID
        )
        print(f"  密钥ID: {read_api_key.id}")
        print(f"  密钥类型: {read_api_key.type}")
        print(f"  密钥令牌: {read_api_key.token}")
        if read_api_key.last_used_at:
            print(f"  最后使用时间: {read_api_key.last_used_at}")
        print(f"  创建时间: {read_api_key.created_at}")
        print()
    except Exception as e:
        print(f"  创建只读API密钥失败: {e}")
    

    print("\n注意: 请妥善保存上述API密钥，它们只会显示一次！")


if __name__ == "__main__":
    asyncio.run(main()) 