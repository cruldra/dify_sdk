"""
Dify SDK - 文件上传示例

本示例展示如何使用upload方法上传文件到Dify平台
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.file import DifyFile


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用upload方法上传文件到Dify平台"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyFile
    dify_file = DifyFile(admin_client)
    
    print("文件上传示例")
    print("-" * 30)
    
    # 准备上传的文件路径
    # 注意：请将此路径替换为您实际要上传的文件路径
    file_path = "examples/file/test_upload.txt"
    
    # 如果测试文件不存在，则创建一个
    if not os.path.exists(file_path):
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 创建测试文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("这是一个测试上传的文件内容。\n")
            f.write("This is a test file content for upload.\n")
        print(f"已创建测试文件: {file_path}")
    
    print(f"\n1. 上传文件 (默认source=datasets):")
    try:
        # 上传文件
        result = await dify_file.upload(file_path)
        
        # 打印上传结果
        print(f"  上传成功!")
        print(f"  文件ID: {result.id}")
        print(f"  文件名: {result.name}")
        print(f"  文件大小: {result.size} 字节")
        print(f"  文件类型: {result.mime_type}")
        print(f"  文件扩展名: {result.extension}")
        
    except Exception as e:
        print(f"  上传文件时出错: {e}")
    
    print("\n2. 上传文件到不同的source:")
    try:
        # 上传文件到不同的source
        result = await dify_file.upload(file_path, source="app")
        print(f"  上传成功! 文件ID: {result.id}")
        
    except Exception as e:
        print(f"  上传文件时出错: {e}")
    
    print("\n3. 尝试上传不存在的文件:")
    non_existent_file = "non_existent_file.txt"
    try:
        result = await dify_file.upload(non_existent_file)
        print(f"  上传成功! 文件ID: {result.id}")
    except Exception as e:
        print(f"  预期的错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 