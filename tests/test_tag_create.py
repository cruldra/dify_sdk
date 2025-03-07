"""
测试标签创建功能
"""

import pytest
from unittest.mock import AsyncMock, patch

from dify.tag import DifyTag
from dify.tag.schemas import Tag, TagType


@pytest.mark.asyncio
async def test_create():
    """测试create方法"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟响应数据
    mock_response = {
        "id": "test_tag_id",
        "name": "测试标签",
        "type": "app",
        "binding_count": 0
    }
    
    # 设置模拟方法的返回值
    mock_admin_client.post.return_value = mock_response
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 调用create方法
    tag_name = "测试标签"
    tag_type = TagType.APP
    result = await dify_tag.create(tag_name, tag_type)
    
    # 验证结果
    assert isinstance(result, Tag)
    assert result.id == "test_tag_id"
    assert result.name == "测试标签"
    assert result.type == "app"
    assert result.binding_count == 0
    
    # 验证调用了正确的API路径和参数
    mock_admin_client.post.assert_called_once_with(
        "/tags", 
        json={"name": tag_name, "type": tag_type.value}
    )


@pytest.mark.asyncio
async def test_create_knowledge_tag():
    """测试create方法，创建知识库标签"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟响应数据
    mock_response = {
        "id": "test_knowledge_tag_id",
        "name": "测试知识库标签",
        "type": "knowledge",
        "binding_count": 0
    }
    
    # 设置模拟方法的返回值
    mock_admin_client.post.return_value = mock_response
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 调用create方法
    tag_name = "测试知识库标签"
    tag_type = TagType.KNOWLEDGE
    result = await dify_tag.create(tag_name, tag_type)
    
    # 验证结果
    assert isinstance(result, Tag)
    assert result.id == "test_knowledge_tag_id"
    assert result.name == "测试知识库标签"
    assert result.type == "knowledge"
    
    # 验证调用了正确的API路径和参数
    mock_admin_client.post.assert_called_once_with(
        "/tags", 
        json={"name": tag_name, "type": tag_type.value}
    )


@pytest.mark.asyncio
async def test_create_empty_name():
    """测试create方法，当标签名称为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 调用create方法，应该抛出ValueError
    with pytest.raises(ValueError, match="标签名称不能为空"):
        await dify_tag.create("", TagType.APP)


@pytest.mark.asyncio
async def test_create_empty_type():
    """测试create方法，当标签类型为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 调用create方法，应该抛出ValueError
    with pytest.raises(ValueError, match="标签类型不能为空"):
        await dify_tag.create("测试标签", None)


@pytest.mark.asyncio
async def test_create_http_error():
    """测试create方法，当HTTP请求失败时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟方法抛出异常
    import httpx
    mock_admin_client.post.side_effect = httpx.HTTPStatusError(
        "400 Bad Request", 
        request=httpx.Request("POST", "http://example.com"), 
        response=httpx.Response(400)
    )
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 调用create方法，应该抛出HTTPStatusError
    with pytest.raises(httpx.HTTPStatusError):
        await dify_tag.create("测试标签", TagType.APP) 