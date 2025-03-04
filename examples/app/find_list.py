"""
Dify SDK - 获取应用列表示例

本示例展示如何使用find_list方法获取Dify应用列表
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.app import DifyApp


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用find_list方法获取Dify应用列表"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyApp
    dify_app = DifyApp(admin_client)
    
    print("获取应用列表示例")
    print("-" * 30)
    
    # 获取应用列表（默认参数）
    print("1. 获取所有应用（默认参数）:")
    app_list = await dify_app.find_list()
    print(f"  总应用数: {app_list.total}")
    print(f"  当前页应用数: {len(app_list.data)}")
    print()
    
    # 按名称搜索应用
    search_term = "助手"  # 可以根据实际情况修改搜索词
    print(f"2. 搜索名称包含 '{search_term}' 的应用:")
    filtered_apps = await dify_app.find_list(name=search_term)
    print(f"  找到 {len(filtered_apps.data)} 个匹配的应用")
    
    # 打印搜索结果
    if filtered_apps.data:
        print("  搜索结果:")
        for i, app in enumerate(filtered_apps.data, 1):
            print(f"  {i}. {app.name} (ID: {app.id})")
    print()
    
    # 按模式过滤应用
    print("3. 获取聊天模式(chat)的应用:")
    chat_apps = await dify_app.find_list(mode="chat")
    print(f"  找到 {len(chat_apps.data)} 个聊天模式应用")
    print()
    
    # 分页获取应用
    page_size = 5
    print(f"4. 分页获取应用（每页 {page_size} 个）:")
    page1 = await dify_app.find_list(page=1, limit=page_size)
    print(f"  第1页: {len(page1.data)} 个应用")
    
    # 如果有更多页，获取第二页
    if page1.total > page_size:
        page2 = await dify_app.find_list(page=2, limit=page_size)
        print(f"  第2页: {len(page2.data)} 个应用")
    print()
    
    # 获取由我创建的应用
    print("5. 获取由我创建的应用:")
    my_apps = await dify_app.find_list(is_created_by_me=True)
    print(f"  我创建的应用数量: {len(my_apps.data)}")


if __name__ == "__main__":
    asyncio.run(main()) 