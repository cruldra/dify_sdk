"""
Dify SDK - 获取单个应用详情示例

本示例展示如何使用find_by_id方法获取Dify单个应用的详细信息
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
    """演示如何使用find_by_id方法获取Dify应用详情"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyApp
    dify_app = DifyApp(admin_client)
    
    print("获取单个应用详情示例")
    print("-" * 30)
    
    # 首先获取应用列表，以便获取一个有效的应用ID
    app_list = await dify_app.find_list(limit=1)
    
    if not app_list.data:
        print("未找到任何应用，请确保您的账户中有创建的应用")
        return
    
    # 获取第一个应用的ID
    app_id = app_list.data[0].id
    
    print(f"1. 获取应用详情 (ID: {app_id}):")
    try:
        app = await dify_app.find_by_id(app_id)
        
        # 打印应用基本信息
        print(f"  应用名称: {app.name}")
        print(f"  应用描述: {app.description}")
        print(f"  应用模式: {app.mode}")
        print(f"  创建时间: {app.created_at}")
        
        # 打印应用配置信息
        print("\n  应用配置:")
        if app.app_config and app.app_config.opening_statement:
            print(f"    开场白: {app.app_config.opening_statement}")
        
        # 打印标签信息
        if app.tags:
            print("\n  应用标签:")
            for i, tag in enumerate(app.tags, 1):
                print(f"    {i}. {tag.name} (类型: {tag.type})")
        
    except Exception as e:
        print(f"获取应用详情时出错: {e}")
    
    print("\n2. 尝试获取不存在的应用:")
    invalid_id = "non_existent_app_id"
    try:
        app = await dify_app.find_by_id(invalid_id)
        print(f"  应用名称: {app.name}")
    except Exception as e:
        print(f"  预期的错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 