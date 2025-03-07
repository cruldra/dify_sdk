"""
Dify SDK - 创建标签示例

本示例展示如何使用create方法创建Dify标签
"""

import asyncio
import os
import random
import string
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.tag import DifyTag
from dify.tag.schemas import TagType


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用create方法创建Dify标签"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyTag
    dify_tag = DifyTag(admin_client)
    
    print("创建标签示例")
    print("-" * 30)
    
    # 生成随机标签名称，避免重复
    random_suffix = ''.join(random.choices(string.digits, k=8))
    knowledge_tag_name = f"测试知识库标签_{random_suffix}"

    # 创建知识库标签
    print(f"\n2. 创建知识库标签 (名称: {knowledge_tag_name}):")
    try:
        knowledge_tag = await dify_tag.create(knowledge_tag_name, TagType.KNOWLEDGE)
        print(f"  创建成功!")
        print(f"  标签ID: {knowledge_tag.id}")
        print(f"  标签名称: {knowledge_tag.name}")
        print(f"  标签类型: {knowledge_tag.type}")
        print(f"  绑定数量: {knowledge_tag.binding_count}")
        
    except Exception as e:
        print(f"  创建知识库标签时出错: {e}")
    
    # 尝试创建空名称的标签
    print("\n3. 尝试创建空名称的标签:")
    try:
        empty_tag = await dify_tag.create("", TagType.APP)
        print(f"  创建成功! 标签ID: {empty_tag.id}")
    except ValueError as e:
        print(f"  预期的错误: {e}")
    
    # 验证标签是否已创建
    print("\n4. 验证标签是否已创建:")
    try:

        # 获取知识库标签列表
        knowledge_tags = await dify_tag.list(TagType.KNOWLEDGE)
        print(f"  知识库标签数量: {len(knowledge_tags)}")
        
        # 检查是否包含我们刚创建的标签
        found_knowledge_tag = False
        for tag in knowledge_tags:
            if tag.name == knowledge_tag_name:
                found_knowledge_tag = True
                break
        
        print(f"  找到新创建的知识库标签: {found_knowledge_tag}")
        
    except Exception as e:
        print(f"  验证过程中出错: {e}")
    
    # 清理创建的标签
    print("\n5. 清理创建的标签:")
    try:

        
        # 删除知识库标签
        for tag in knowledge_tags:
            if tag.name == knowledge_tag_name:
                result = await dify_tag.delete(tag.id)
                print(f"  删除知识库标签 '{knowledge_tag_name}': {'成功' if result else '失败'}")
        
    except Exception as e:
        print(f"  清理过程中出错: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 