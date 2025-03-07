"""
Dify SDK - 标签绑定示例

本示例展示如何使用bind方法将标签绑定到目标对象
"""

import asyncio
import os
import random
import string
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.tag import DifyTag
from dify.tag.schemas import TagType, BindingPayloads
from dify.dataset import DifyDataset


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用bind方法将标签绑定到目标对象"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyTag和DifyDataset
    dify_tag = DifyTag(admin_client)
    dify_dataset = DifyDataset(admin_client)
    
    print("标签绑定示例")
    print("-" * 30)
    
    # 步骤1: 获取知识库列表，以便获取一个有效的知识库ID
    print("1. 获取知识库列表:")
    try:
        # 这里假设DifyDataset类有find_list方法，如果没有，请替换为适当的方法
        # datasets = await dify_dataset.find_list()
        # 由于可能没有find_list方法，这里使用一个示例ID
        dataset_id = "your_dataset_id_here"  # 请替换为实际的知识库ID
        print(f"  选择知识库ID: {dataset_id}")
        
    except Exception as e:
        print(f"  获取知识库列表时出错: {e}")
        return
    
    # 步骤2: 创建一个测试标签
    print("\n2. 创建测试标签:")
    try:
        # 生成随机标签名称，避免重复
        random_suffix = ''.join(random.choices(string.digits, k=8))
        tag_name = f"测试标签_{random_suffix}"
        
        # 创建知识库标签
        tag = await dify_tag.create(tag_name, TagType.KNOWLEDGE)
        tag_id = tag.id
        print(f"  创建成功! 标签ID: {tag_id}, 名称: {tag.name}")
        
    except Exception as e:
        print(f"  创建标签时出错: {e}")
        return
    
    # 步骤3: 绑定标签到知识库
    print(f"\n3. 绑定标签到知识库 (标签ID: {tag_id}, 知识库ID: {dataset_id}):")
    try:
        # 创建绑定参数
        binding_payload = BindingPayloads(
            tag_ids=[tag_id],
            target_id=dataset_id,
            type=TagType.KNOWLEDGE
        )
        
        # 绑定标签
        result = await dify_tag.bind(binding_payload)
        print(f"  绑定结果: {'成功' if result else '失败'}")
        
    except Exception as e:
        print(f"  绑定标签时出错: {e}")
    
    # 步骤4: 尝试使用无效参数绑定标签
    print("\n4. 尝试使用空标签ID列表绑定标签:")
    try:
        invalid_payload = BindingPayloads(
            tag_ids=[],
            target_id=dataset_id,
            type=TagType.KNOWLEDGE
        )
        result = await dify_tag.bind(invalid_payload)
        print(f"  绑定结果: {'成功' if result else '失败'}")
    except ValueError as e:
        print(f"  预期的错误: {e}")
    
    # 步骤5: 清理创建的标签
    print("\n5. 清理创建的标签:")
    try:
        # 删除标签
        result = await dify_tag.delete(tag_id)
        print(f"  删除标签 '{tag_name}': {'成功' if result else '失败'}")
        
    except Exception as e:
        print(f"  清理过程中出错: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 