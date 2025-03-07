"""
Dify SDK - 删除知识库示例

本示例展示如何使用delete方法删除Dify知识库
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.dataset import DifyDataset


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用delete方法删除Dify知识库"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyDataset
    dify_dataset = DifyDataset(admin_client)
    
    print("删除知识库示例")
    print("-" * 30)
    
    # 请替换为您要删除的知识库ID
    dataset_id = "aff19d02-82e2-41ae-b648-d34c230639ff"
    
    print(f"1. 删除知识库 (ID: {dataset_id}):")
    try:
        # 删除知识库
        result = await dify_dataset.delete(dataset_id)
        print(f"  删除结果: {'成功' if result else '失败'}")
        
    except Exception as e:
        print(f"  删除知识库时出错: {e}")
    
    print("\n2. 尝试删除不存在的知识库:")
    invalid_id = "non_existent_dataset_id"
    try:
        result = await dify_dataset.delete(invalid_id)
        print(f"  删除结果: {'成功' if result else '失败'}")
    except Exception as e:
        print(f"  预期的错误: {e}")
    
    print("\n3. 尝试使用空ID删除知识库:")
    try:
        result = await dify_dataset.delete("")
        print(f"  删除结果: {'成功' if result else '失败'}")
    except ValueError as e:
        print(f"  预期的错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 