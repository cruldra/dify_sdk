"""
Dify SDK - 获取LLM模型列表示例

本示例展示如何使用find_list方法获取Dify支持的LLM模型列表
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.llm import LLM


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用find_list方法获取Dify支持的LLM模型列表"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化LLM
    llm = LLM(admin_client)
    
    print("获取LLM模型列表示例")
    print("-" * 30)
    
    # 获取LLM模型列表
    print("获取所有支持的LLM模型:")
    try:
        llm_list = await llm.find_list()
        print(f"找到 {len(llm_list.data)} 个LLM模型提供者")
        
        # 打印每个模型提供者的信息
        for i, provider in enumerate(llm_list.data, 1):
            print(f"\n{i}. 提供者: {provider.provider}")
            print(f"   标签: {provider.label.zh_Hans or provider.label.en_US}")
            print(f"   状态: {provider.status}")
            
            # 打印该提供者下的模型
            print(f"   模型列表 ({len(provider.models)}个):")
            for j, model in enumerate(provider.models, 1):
                model_label = model.label.zh_Hans or model.label.en_US
                print(f"     {j}. {model.model} - {model_label}")
                print(f"        类型: {model.model_type}")
                print(f"        功能: {', '.join(model.features)}")
                print(f"        状态: {model.status}")
                if model.model_properties and model.model_properties.context_size:
                    print(f"        上下文大小: {model.model_properties.context_size}")
                print()
    
    except Exception as e:
        print(f"获取LLM模型列表时出错: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 