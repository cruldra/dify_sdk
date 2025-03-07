"""
测试LLM模块的功能
"""

import pytest
from unittest.mock import AsyncMock, patch

from dify.llm import LLM
from dify.llm.schemas import LLMList


@pytest.mark.asyncio
async def test_find_list():
    """测试find_list方法"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟响应数据
    mock_response = {
        "data": [
            {
                "tenant_id": "test-tenant-id",
                "provider": "openai",
                "label": {
                    "zh_Hans": "OpenAI",
                    "en_US": "OpenAI"
                },
                "icon_small": {
                    "zh_Hans": "icon-url-small-zh",
                    "en_US": "icon-url-small-en"
                },
                "icon_large": {
                    "zh_Hans": "icon-url-large-zh",
                    "en_US": "icon-url-large-en"
                },
                "status": "active",
                "models": [
                    {
                        "model": "gpt-3.5-turbo",
                        "label": {
                            "zh_Hans": "GPT-3.5 Turbo",
                            "en_US": "GPT-3.5 Turbo"
                        },
                        "model_type": "chat",
                        "features": ["chat", "completion"],
                        "fetch_from": "openai",
                        "model_properties": {
                            "context_size": 4096,
                            "mode": "chat"
                        },
                        "deprecated": False,
                        "status": "active",
                        "load_balancing_enabled": False
                    }
                ]
            }
        ]
    }
    
    # 设置模拟方法的返回值
    mock_admin_client.get.return_value = mock_response
    
    # 创建LLM实例
    llm = LLM(mock_admin_client)
    
    # 调用find_list方法
    result = await llm.find_list()
    
    # 验证结果
    assert isinstance(result, LLMList)
    assert len(result.data) == 1
    assert result.data[0].provider == "openai"
    assert result.data[0].label.zh_Hans == "OpenAI"
    assert len(result.data[0].models) == 1
    assert result.data[0].models[0].model == "gpt-3.5-turbo"
    
    # 验证调用了正确的API路径
    mock_admin_client.get.assert_called_once_with(
        "/workspaces/current/models/model-types/llm",
    ) 