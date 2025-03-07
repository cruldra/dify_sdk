"""
Dify SDK - 查询知识库列表示例

本示例展示如何使用find_list方法查询Dify知识库列表
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.dataset import DifyDataset
from dify.tag import DifyTag
from dify.tag.schemas import TagType


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用find_list方法查询Dify知识库列表"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyDataset和DifyTag
    dify_dataset = DifyDataset(admin_client)
    dify_tag = DifyTag(admin_client)
    
    print("查询知识库列表示例")
    print("-" * 30)
    
    # 查询所有知识库
    print("1. 查询所有知识库（默认参数）:")
    try:
        dataset_list = await dify_dataset.find_list()
        print(f"  总知识库数: {dataset_list.total}")
        print(f"  当前页知识库数: {len(dataset_list.data)}")
        print(f"  是否有更多: {dataset_list.has_more}")
        
        # 打印知识库信息
        if dataset_list.data:
            print("\n  知识库列表:")
            for i, dataset in enumerate(dataset_list.data, 1):
                print(f"    {i}. ID: {dataset.id}")
                print(f"       名称: {dataset.name}")
                print(f"       描述: {dataset.description}")
                print()
        
    except Exception as e:
        print(f"  查询知识库列表时出错: {e}")
    
    # 分页查询知识库
    print("\n2. 分页查询知识库:")
    try:
        page = 1
        limit = 5
        dataset_list = await dify_dataset.find_list(page=page, limit=limit)
        print(f"  第{page}页（每页{limit}条）:")
        print(f"  总知识库数: {dataset_list.total}")
        print(f"  当前页知识库数: {len(dataset_list.data)}")
        print(f"  是否有更多: {dataset_list.has_more}")
        
    except Exception as e:
        print(f"  分页查询知识库时出错: {e}")
    
    # 根据标签查询知识库
    print("\n3. 根据标签查询知识库:")
    try:
        # 首先获取知识库标签列表
        tags = await dify_tag.list(TagType.KNOWLEDGE)
        
        if not tags:
            print("  未找到任何知识库标签，无法进行标签筛选")
        else:
            # 使用第一个标签进行筛选
            tag = tags[0]
            print(f"  使用标签 '{tag.name}' (ID: {tag.id}) 进行筛选:")
            
            # 根据标签ID查询知识库
            dataset_list = await dify_dataset.find_list(tag_ids=[tag.id])
            print(f"  找到 {dataset_list.total} 个知识库")
            
            # 打印知识库信息
            if dataset_list.data:
                print("\n  知识库列表:")
                for i, dataset in enumerate(dataset_list.data, 1):
                    print(f"    {i}. ID: {dataset.id}")
                    print(f"       名称: {dataset.name}")
                    print()
            
    except Exception as e:
        print(f"  根据标签查询知识库时出错: {e}")
    
    # 查询所有知识库（包括共享的）
    print("\n4. 查询所有知识库（包括共享的）:")
    try:
        dataset_list = await dify_dataset.find_list(include_all=True)
        print(f"  总知识库数: {dataset_list.total}")
        print(f"  当前页知识库数: {len(dataset_list.data)}")
        
    except Exception as e:
        print(f"  查询所有知识库时出错: {e}")
    
    # 尝试使用无效参数查询知识库
    print("\n5. 尝试使用无效参数查询知识库:")
    try:
        dataset_list = await dify_dataset.find_list(page=0)
        print(f"  总知识库数: {dataset_list.total}")
    except ValueError as e:
        print(f"  预期的错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 