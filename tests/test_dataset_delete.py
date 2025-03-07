"""
测试知识库删除功能
"""

import pytest
from unittest.mock import AsyncMock, patch

from dify.dataset import DifyDataset


@pytest.mark.asyncio
async def test_delete():
    """测试delete方法"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟方法的返回值
    mock_admin_client.delete.return_value = None  # DELETE请求通常不返回内容
    
    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)
    
    # 调用delete方法
    dataset_id = "test_dataset_id"
    result = await dify_dataset.delete(dataset_id)
    
    # 验证结果
    assert result is True
    
    # 验证调用了正确的API路径
    mock_admin_client.delete.assert_called_once_with(f"/datasets/{dataset_id}")


@pytest.mark.asyncio
async def test_delete_empty_dataset_id():
    """测试delete方法，当知识库ID为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)
    
    # 调用delete方法，应该抛出ValueError
    with pytest.raises(ValueError, match="知识库ID不能为空"):
        await dify_dataset.delete("")


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
    
    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)
    
    # 调用delete方法，应该抛出HTTPStatusError
    dataset_id = "non_existent_dataset_id"
    with pytest.raises(httpx.HTTPStatusError):
        await dify_dataset.delete(dataset_id) 