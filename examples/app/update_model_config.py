"""
Dify SDK - 更新应用模型配置示例

本示例展示如何使用update_model_config方法更新Dify应用的模型配置
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.app import DifyApp
from dify.app.schemas import ModelConfigUpdatePayload, ModelInUpdate


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用update_model_config方法更新Dify应用的模型配置"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyApp
    dify_app = DifyApp(admin_client)
    
    print("更新应用模型配置示例")
    print("-" * 30)
    
    # 首先获取应用列表，以便获取一个有效的应用ID
    app_list = await dify_app.find_list(limit=1)
    
    if not app_list.data:
        print("未找到任何应用，请确保您的账户中有创建的应用")
        return
    
    # 获取第一个应用的ID
    app_id = app_list.data[0].id
    
    print(f"1. 准备更新应用模型配置 (ID: {app_id}):")
    
    # 创建模型配置更新对象
    model_config = ModelConfigUpdatePayload(
        pre_prompt="这是一个更新后的预设提示词",
        prompt_type="simple",
        opening_statement="欢迎使用更新后的应用！",
        suggested_questions=["您可以问我什么问题？", "如何使用这个应用？"],
        more_like_this={"enabled": False},
        sensitive_word_avoidance={"enabled": False, "type": "", "configs": []},
        speech_to_text={"enabled": False},
        text_to_speech={"enabled": False},
        file_upload={
            "image": {
                "detail": "high",
                "enabled": False,
                "number_limits": 3,
                "transfer_methods": ["remote_url", "local_file"]
            },
            "enabled": False,
            "allowed_file_types": [],
            "allowed_file_extensions": [".JPG", ".JPEG", ".PNG", ".GIF", ".WEBP", ".SVG", ".MP4", ".MOV", ".MPEG", ".MPGA"],
            "allowed_file_upload_methods": ["remote_url", "local_file"],
            "number_limits": 3
        },
        suggested_questions_after_answer={"enabled": False},
        retriever_resource={"enabled": True},
        agent_mode={"enabled": False, "max_iteration": 5, "strategy": "react", "tools": []},
        model=ModelInUpdate(
            provider="langgenius/openai/openai",
            name="gpt-3.5-turbo-instruct",
            mode="completion",
            completion_params={}
        ),
        dataset_configs={
            "retrieval_model": "multiple",
            "top_k": 4,
            "reranking_enable": False,
            "datasets": {"datasets": []}
        }
    )
    
    try:
        # 更新应用模型配置
        result = await dify_app.update_model_config(app_id, model_config)
        print(f"  更新结果: {result.result}")
        print("  应用模型配置已成功更新！")
        
    except Exception as e:
        print(f"  更新应用模型配置时出错: {e}")
    
    print("\n2. 尝试使用无效的应用ID更新模型配置:")
    invalid_id = "non_existent_app_id"
    try:
        result = await dify_app.update_model_config(invalid_id, model_config)
        print(f"  更新结果: {result.result}")
    except Exception as e:
        print(f"  预期的错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 