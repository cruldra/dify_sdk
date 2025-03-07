"""
测试应用模型配置更新功能
"""

import pytest
from unittest.mock import AsyncMock, patch

from dify.app import DifyApp
from dify.app.schemas import ModelConfigUpdatePayload, ModelInUpdate, OperationResult


@pytest.mark.asyncio
async def test_update_model_config():
    """测试update_model_config方法"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟响应数据
    mock_response = {"result": "success"}
    
    # 设置模拟方法的返回值
    mock_admin_client.post.return_value = mock_response
    
    # 创建DifyApp实例
    dify_app = DifyApp(mock_admin_client)
    
    # 创建模型配置更新对象
    model_config = ModelConfigUpdatePayload(
        pre_prompt="测试预设提示词",
        prompt_type="simple",
        opening_statement="测试开场白",
        suggested_questions=["测试问题1", "测试问题2"],
        model=ModelInUpdate(
            provider="test_provider",
            name="test_model",
            mode="completion",
            completion_params={}
        )
    )
    
    # 调用update_model_config方法
    app_id = "test_app_id"
    result = await dify_app.update_model_config(app_id, model_config)
    
    # 验证结果
    assert isinstance(result, OperationResult)
    assert result.result == "success"
    
    # 验证调用了正确的API路径和参数
    mock_admin_client.post.assert_called_once()
    call_args = mock_admin_client.post.call_args
    assert call_args[0][0] == f"/apps/{app_id}/model-config"
    
    # 验证传递的JSON数据
    json_data = call_args[1]["json"]
    assert json_data["pre_prompt"] == "测试预设提示词"
    assert json_data["prompt_type"] == "simple"
    assert json_data["opening_statement"] == "测试开场白"
    assert len(json_data["suggested_questions"]) == 2
    assert json_data["model"]["provider"] == "test_provider"
    assert json_data["model"]["name"] == "test_model"
    assert json_data["model"]["mode"] == "completion"


@pytest.mark.asyncio
async def test_update_model_config_empty_app_id():
    """测试update_model_config方法，当应用ID为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyApp实例
    dify_app = DifyApp(mock_admin_client)
    
    # 创建模型配置更新对象
    model_config = ModelConfigUpdatePayload(
        pre_prompt="测试预设提示词",
        prompt_type="simple"
    )
    
    # 调用update_model_config方法，应该抛出ValueError
    with pytest.raises(ValueError, match="应用ID不能为空"):
        await dify_app.update_model_config("", model_config) 