"""
Dify SDK - 创建知识库示例

本示例展示如何使用create方法创建Dify知识库
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.file import DifyFile
from dify.dataset import DifyDataset
from dify.dataset.schemas import (
    DataSetCreatePayloads,
    DataSource,
    InfoList,
    FileInfoList,
    ProcessRule,
    RetrievalModel,
)


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用create方法创建Dify知识库"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyFile和DifyDataset
    dify_file = DifyFile(admin_client)
    dify_dataset = DifyDataset(admin_client)
    
    print("创建知识库示例")
    print("-" * 30)
    
    # 首先上传一个测试文件
    print("1. 上传测试文件:")
    
    # 创建一个测试文件
    test_file_path = "examples/dataset/test_file.txt"
    if not os.path.exists(test_file_path):
        # 确保目录存在
        os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
        
        # 创建测试文件
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("这是一个测试知识库的文件内容。\n")
            f.write("包含一些示例文本，用于创建知识库。\n")
            f.write("Dify是一个强大的AI应用开发平台。\n")
        print(f"已创建测试文件: {test_file_path}")
    
    try:
        # 上传文件
        file_result = await dify_file.upload(test_file_path)
        file_id = file_result.id
        print(f"  文件上传成功! 文件ID: {file_id}")
        
        # 创建知识库参数
        print("\n2. 创建知识库:")
        create_payload = DataSetCreatePayloads(
            data_source=DataSource(
                type="upload_file",
                info_list=InfoList(
                    data_source_type="upload_file",
                    file_info_list=FileInfoList(
                        file_ids=[file_id]
                    )
                )
            ),
            indexing_technique="high_quality",
            process_rule=ProcessRule(
                rules={
                    "pre_processing_rules": [
                        {"id": "remove_extra_spaces", "enabled": True},
                        {"id": "remove_urls_emails", "enabled": False}
                    ],
                    "segmentation": {
                        "separator": "\n\n",
                        "max_tokens": 500,
                        "chunk_overlap": 50
                    }
                },
                mode="custom"
            ),
            doc_form="text_model",
            doc_language="Chinese",
            retrieval_model=RetrievalModel(
                search_method="hybrid_search",
                reranking_enable=True,
                top_k=3,
                score_threshold_enabled=False,
                score_threshold=0.5
            ),
            embedding_model="text-embedding-3-large",
            embedding_model_provider="langgenius/openai/openai"
        )
        
        # 创建知识库
        result = await dify_dataset.create(create_payload)
        
        # 打印创建结果
        print(f"  知识库创建成功!")
        print(f"  知识库ID: {result.dataset.id}")
        print(f"  知识库名称: {result.dataset.name}")
        print(f"  索引技术: {result.dataset.indexing_technique}")
        print(f"  文档数量: {len(result.documents)}")
        
        # 打印文档信息
        if result.documents:
            print("\n  文档信息:")
            for i, doc in enumerate(result.documents, 1):
                print(f"    {i}. 文档ID: {doc.id}")
                print(f"       文档名称: {doc.name}")
                print(f"       索引状态: {doc.indexing_status}")
                print(f"       创建时间: {doc.created_at}")
                print()
        
    except Exception as e:
        print(f"操作过程中出错: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 