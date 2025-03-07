"""
Dify SDK - 获取标签列表示例

本示例展示如何使用list方法获取Dify标签列表
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.tag import DifyTag, TagType

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用list方法获取Dify标签列表"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyTag
    dify_tag = DifyTag(admin_client)
    
    print("获取标签列表示例")
    print("-" * 30)
    
    # 获取应用标签列表
    print("1. 获取应用标签列表:")
    try:
        app_tags = await dify_tag.list(TagType.APP)
        print(f"  找到 {len(app_tags)} 个应用标签")
        
        # 打印标签信息
        if app_tags:
            print("\n  应用标签列表:")
            for i, tag in enumerate(app_tags, 1):
                print(f"    {i}. ID: {tag.id}")
                print(f"       名称: {tag.name}")
                print(f"       类型: {tag.type}")
                print()
        
    except Exception as e:
        print(f"  获取应用标签列表时出错: {e}")
    
    # 获取知识库标签列表
    print("\n2. 获取知识库标签列表:")
    try:
        dataset_tags = await dify_tag.list(TagType.KNOWLEDGE)
        print(f"  找到 {len(dataset_tags)} 个知识库标签")
        
        # 打印标签信息
        if dataset_tags:
            print("\n  知识库标签列表:")
            for i, tag in enumerate(dataset_tags, 1):
                print(f"    {i}. ID: {tag.id}")
                print(f"       名称: {tag.name}")
                print(f"       类型: {tag.type}")
                print()
        
    except Exception as e:
        print(f"  获取知识库标签列表时出错: {e}")
    


if __name__ == "__main__":
    asyncio.run(main()) 