"""
测试应用删除功能
"""

import pytest
from unittest.mock import AsyncMock, patch

from dify.app import DifyApp


@pytest.mark.asyncio
async def test_delete():
    """测试delete方法"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟方法的返回值
    mock_admin_client.delete.return_value = None  # DELETE请求通常不返回内容
    
    # 创建DifyApp实例
    dify_app = DifyApp(mock_admin_client)
    
    # 调用delete方法
    app_id = "test_app_id"
    result = await dify_app.delete(app_id)
    
    # 验证结果
    assert result is True
    
    # 验证调用了正确的API路径
    mock_admin_client.delete.assert_called_once_with(f"/apps/{app_id}")


@pytest.mark.asyncio
async def test_delete_empty_app_id():
    """测试delete方法，当应用ID为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyApp实例
    dify_app = DifyApp(mock_admin_client)
    
    # 调用delete方法，应该抛出ValueError
    with pytest.raises(ValueError, match="应用ID不能为空"):
        await dify_app.delete("")


@pytest.mark.asyncio
async def test_delete_http_error():
    """测试delete方法，当HTTP请求失败时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟方法抛出异常
    import httpx
    mock_admin_client.delete.side_effect = httpx.HTTPStatusError(
        "404 Not Found", 
        request=httpx.Request("DELETE", "http://example.com"), 
        response=httpx.Response(404)
    )
    
    # 创建DifyApp实例
    dify_app = DifyApp(mock_admin_client)
    
    # 调用delete方法，应该抛出HTTPStatusError
    app_id = "non_existent_app_id"
    with pytest.raises(httpx.HTTPStatusError):
        await dify_app.delete(app_id) 