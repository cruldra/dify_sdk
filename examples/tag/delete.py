"""
Dify SDK - 删除标签示例

本示例展示如何使用delete方法删除Dify标签
"""

import asyncio
import os
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
    """演示如何使用delete方法删除Dify标签"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyTag
    dify_tag = DifyTag(admin_client)
    
    print("删除标签示例")
    print("-" * 30)
    
    # 首先获取知识库标签列表
    print("1. 获取知识库标签列表:")
    try:
        knowledge_tags = await dify_tag.list(TagType.KNOWLEDGE)
        print(f"  找到 {len(knowledge_tags)} 个知识库标签")
        
        if not knowledge_tags:
            print("  未找到任何知识库标签，无法进行删除操作")
            return
        
        print("\n2. 删除知识库标签:")
        
        # 遍历所有知识库标签并删除
        for i, tag in enumerate(knowledge_tags, 1):
            tag_id = tag.id
            tag_name = tag.name
            
            print(f"  {i}. 删除标签 (ID: {tag_id}, 名称: {tag_name}):")
            
            try:
                # 实际删除标签
                result = await dify_tag.delete(tag_id)
                print(f"    删除结果: {'成功' if result else '失败'}")
            except Exception as e:
                print(f"    删除失败: {e}")
        
    except Exception as e:
        print(f"  操作过程中出错: {e}")
    
    # 验证知识库标签是否已全部删除
    print("\n3. 验证知识库标签是否已全部删除:")
    try:
        remaining_tags = await dify_tag.list(TagType.KNOWLEDGE)
        print(f"  剩余知识库标签数量: {len(remaining_tags)}")
        
        if remaining_tags:
            print("  以下知识库标签未被删除:")
            for i, tag in enumerate(remaining_tags, 1):
                print(f"    {i}. ID: {tag.id}, 名称: {tag.name}")
        else:
            print("  所有知识库标签已成功删除")
        
    except Exception as e:
        print(f"  验证过程中出错: {e}")
    
    # 尝试删除不存在的标签
    print("\n4. 尝试删除不存在的标签:")
    invalid_id = "non_existent_tag_id"
    try:
        result = await dify_tag.delete(invalid_id)
        print(f"  删除结果: {'成功' if result else '失败'}")
    except Exception as e:
        print(f"  预期的错误: {e}")
    
    # 尝试使用空ID删除标签
    print("\n5. 尝试使用空ID删除标签:")
    try:
        result = await dify_tag.delete("")
        print(f"  删除结果: {'成功' if result else '失败'}")
    except ValueError as e:
        print(f"  预期的错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 