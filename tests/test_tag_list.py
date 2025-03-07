"""
测试标签列表功能
"""

import pytest
from unittest.mock import AsyncMock, patch

from dify.tag import DifyTag
from dify.tag.schemas import Tag


@pytest.mark.asyncio
async def test_list():
    """测试list方法"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟响应数据
    mock_response = [
        {
            "id": "tag1",
            "name": "标签1",
            "type": "app",
            "binding_count": 5
        },
        {
            "id": "tag2",
            "name": "标签2",
            "type": "app",
            "binding_count": 3
        }
    ]
    
    # 设置模拟方法的返回值
    mock_admin_client.get.return_value = mock_response
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 调用list方法
    tag_type = "app"
    result = await dify_tag.list(tag_type)
    
    # 验证结果
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(tag, Tag) for tag in result)
    assert result[0].id == "tag1"
    assert result[0].name == "标签1"
    assert result[0].type == "app"
    assert result[0].binding_count == 5
    assert result[1].id == "tag2"
    assert result[1].name == "标签2"
    
    # 验证调用了正确的API路径和参数
    mock_admin_client.get.assert_called_once_with("/tags", params={"type": tag_type})


@pytest.mark.asyncio
async def test_list_empty_type():
    """测试list方法，当标签类型为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 调用list方法，应该抛出ValueError
    with pytest.raises(ValueError, match="标签类型不能为空"):
        await dify_tag.list("")


@pytest.mark.asyncio
async def test_list_http_error():
    """测试list方法，当HTTP请求失败时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟方法抛出异常
    import httpx
    mock_admin_client.get.side_effect = httpx.HTTPStatusError(
        "400 Bad Request", 
        request=httpx.Request("GET", "http://example.com"), 
        response=httpx.Response(400)
    )
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 调用list方法，应该抛出HTTPStatusError
    with pytest.raises(httpx.HTTPStatusError):
        await dify_tag.list("app") 