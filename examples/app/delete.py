"""
Dify SDK - 删除应用示例

本示例展示如何使用delete方法删除Dify应用
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


async def main():
    """演示如何使用delete方法删除Dify应用"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyApp
    dify_app = DifyApp(admin_client)
    
    print("删除应用示例")
    print("-" * 30)
    
    # 首先创建一个测试应用，然后删除它
    print("1. 创建测试应用:")
    try:
        # 创建一个测试应用
        test_app = await dify_app.create(
            name="测试删除应用",
            mode="chat",
            description="这是一个用于测试删除功能的应用"
        )
        
        app_id = test_app.id
        print(f"  创建成功! 应用ID: {app_id}")
        print(f"  应用名称: {test_app.name}")
        print(f"  应用模式: {test_app.mode}")
        
        # 删除刚刚创建的应用
        print("\n2. 删除测试应用:")
        result = await dify_app.delete(app_id)
        print(f"  删除结果: {'成功' if result else '失败'}")
        
        # 验证应用是否已被删除
        print("\n3. 验证应用是否已被删除:")
        try:
            app = await dify_app.find_by_id(app_id)
            print(f"  应用仍然存在: {app.name}")
        except Exception as e:
            print(f"  应用已被删除，无法找到: {e}")
        
    except Exception as e:
        print(f"操作过程中出错: {e}")
    
    print("\n4. 尝试删除不存在的应用:")
    invalid_id = "non_existent_app_id"
    try:
        result = await dify_app.delete(invalid_id)
        print(f"  删除结果: {'成功' if result else '失败'}")
    except Exception as e:
        print(f"  预期的错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 