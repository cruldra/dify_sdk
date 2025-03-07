"""
测试标签绑定功能
"""

import pytest
from unittest.mock import AsyncMock, patch

from dify.tag import DifyTag
from dify.tag.schemas import TagType, BindingPayloads


@pytest.mark.asyncio
async def test_bind():
    """测试bind方法"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟方法的返回值
    mock_admin_client.post.return_value = None  # POST请求通常不返回内容
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 创建绑定参数
    tag_ids = ["test_tag_id"]
    target_id = "test_dataset_id"
    tag_type = TagType.KNOWLEDGE
    
    binding_payload = BindingPayloads(
        tag_ids=tag_ids,
        target_id=target_id,
        type=tag_type
    )
    
    # 调用bind方法
    result = await dify_tag.bind(binding_payload)
    
    # 验证结果
    assert result is True
    
    # 验证调用了正确的API路径和参数
    mock_admin_client.post.assert_called_once()
    call_args = mock_admin_client.post.call_args
    assert call_args[0][0] == "/tag-bindings/create"
    
    # 验证传递的JSON数据
    json_data = call_args[1]["json"]
    assert json_data["tag_ids"] == tag_ids
    assert json_data["target_id"] == target_id
    assert json_data["type"] == tag_type.value


@pytest.mark.asyncio
async def test_bind_empty_tag_ids():
    """测试bind方法，当标签ID列表为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 创建绑定参数，标签ID列表为空
    binding_payload = BindingPayloads(
        tag_ids=[],
        target_id="test_dataset_id",
        type=TagType.KNOWLEDGE
    )
    
    # 调用bind方法，应该抛出ValueError
    with pytest.raises(ValueError, match="标签ID列表不能为空"):
        await dify_tag.bind(binding_payload)


@pytest.mark.asyncio
async def test_bind_empty_target_id():
    """测试bind方法，当目标对象ID为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 创建绑定参数，目标对象ID为空
    binding_payload = BindingPayloads(
        tag_ids=["test_tag_id"],
        target_id="",
        type=TagType.KNOWLEDGE
    )
    
    # 调用bind方法，应该抛出ValueError
    with pytest.raises(ValueError, match="目标对象ID不能为空"):
        await dify_tag.bind(binding_payload)


@pytest.mark.asyncio
async def test_bind_empty_type():
    """测试bind方法，当标签类型为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyTag实例
    dify_tag = DifyTag(mock_admin_client)
    
    # 创建绑定参数，标签类型为空
    binding_payload = BindingPayloads(
        tag_ids=["test_tag_id"],
        target_id="test_dataset_id",
        type=None
    )
    
    # 调用bind方法，应该抛出ValueError
    with pytest.raises(ValueError, match="标签类型不能为空"):
        await dify_tag.bind(binding_payload)


@pytest.mark.asyncio
async def test_bind_http_error():
    """测试bind方法，当HTTP请求失败时"""
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
    
    # 创建绑定参数
    binding_payload = BindingPayloads(
        tag_ids=["test_tag_id"],
        target_id="test_dataset_id",
        type=TagType.KNOWLEDGE
    )
    
    # 调用bind方法，应该抛出HTTPStatusError
    with pytest.raises(httpx.HTTPStatusError):
        await dify_tag.bind(binding_payload) 