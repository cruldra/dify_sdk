"""
测试标签删除功能
"""

import pytest
from unittest.mock import AsyncMock, patch

from dify.tag import DifyTag


@pytest.mark.asyncio
async def test_delete():
    """测试delete方法"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟方法的返回值
    mock_admin_client.delete.return_value = None  # DELETE请求通常不返回内容
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 调用delete方法
    tag_id = "test_tag_id"
    result = await dify_tag.delete(tag_id)
    
    # 验证结果
    assert result is True
    
    # 验证调用了正确的API路径
    mock_admin_client.delete.assert_called_once_with(f"/tags/{tag_id}")


@pytest.mark.asyncio
async def test_delete_empty_tag_id():
    """测试delete方法，当标签ID为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 调用delete方法，应该抛出ValueError
    with pytest.raises(ValueError, match="标签ID不能为空"):
        await dify_tag.delete("")


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
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 调用delete方法，应该抛出HTTPStatusError
    tag_id = "non_existent_tag_id"
    with pytest.raises(httpx.HTTPStatusError):
        await dify_tag.delete(tag_id) 