"""
测试知识库列表查询功能
"""

import pytest
from unittest.mock import AsyncMock, patch

from dify.dataset import DifyDataset
from dify.dataset.schemas import DataSetList, DataSet


@pytest.mark.asyncio
async def test_find_list():
    """测试find_list方法"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟响应数据
    mock_response = {
        "data": [
            {
                "id": "test_dataset_id_1",
                "name": "测试知识库1",
                "description": "这是测试知识库1的描述",
                "permission": "only_me",
                "data_source_type": "upload_file",
                "indexing_technique": "high_quality",
                "created_by": "test_user",
                "created_at": 1630000000
            },
            {
                "id": "test_dataset_id_2",
                "name": "测试知识库2",
                "description": "这是测试知识库2的描述",
                "permission": "only_me",
                "data_source_type": "upload_file",
                "indexing_technique": "high_quality",
                "created_by": "test_user",
                "created_at": 1630000001
            }
        ],
        "total": 2,
        "has_more": False
    }
    
    # 设置模拟方法的返回值
    mock_admin_client.get.return_value = mock_response
    
    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)
    
    # 调用find_list方法
    result = await dify_dataset.find_list()
    
    # 验证结果
    assert isinstance(result, DataSetList)
    assert len(result.data) == 2
    assert result.total == 2
    assert result.has_more is False
    assert all(isinstance(dataset, DataSet) for dataset in result.data)
    assert result.data[0].id == "test_dataset_id_1"
    assert result.data[0].name == "测试知识库1"
    assert result.data[1].id == "test_dataset_id_2"
    assert result.data[1].name == "测试知识库2"
    
    # 验证调用了正确的API路径和参数
    mock_admin_client.get.assert_called_once_with(
        "/datasets", 
        params={"page": 1, "limit": 30, "include_all": "false"}
    )


@pytest.mark.asyncio
async def test_find_list_with_pagination():
    """测试find_list方法，使用分页参数"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟响应数据
    mock_response = {
        "data": [
            {
                "id": "test_dataset_id_1",
                "name": "测试知识库1",
                "description": "这是测试知识库1的描述",
                "permission": "only_me",
                "data_source_type": "upload_file",
                "indexing_technique": "high_quality",
                "created_by": "test_user",
                "created_at": 1630000000
            }
        ],
        "total": 10,
        "has_more": True
    }
    
    # 设置模拟方法的返回值
    mock_admin_client.get.return_value = mock_response
    
    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)
    
    # 调用find_list方法，使用分页参数
    page = 2
    limit = 5
    result = await dify_dataset.find_list(page=page, limit=limit)
    
    # 验证结果
    assert isinstance(result, DataSetList)
    assert len(result.data) == 1
    assert result.total == 10
    assert result.has_more is True
    
    # 验证调用了正确的API路径和参数
    mock_admin_client.get.assert_called_once_with(
        "/datasets", 
        params={"page": page, "limit": limit, "include_all": "false"}
    )


@pytest.mark.asyncio
async def test_find_list_with_tag_ids():
    """测试find_list方法，使用标签ID筛选"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟响应数据
    mock_response = {
        "data": [
            {
                "id": "test_dataset_id_1",
                "name": "测试知识库1",
                "description": "这是测试知识库1的描述",
                "permission": "only_me",
                "data_source_type": "upload_file",
                "indexing_technique": "high_quality",
                "created_by": "test_user",
                "created_at": 1630000000
            }
        ],
        "total": 1,
        "has_more": False
    }
    
    # 设置模拟方法的返回值
    mock_admin_client.get.return_value = mock_response
    
    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)
    
    # 调用find_list方法，使用标签ID筛选
    tag_ids = ["test_tag_id_1", "test_tag_id_2"]
    result = await dify_dataset.find_list(tag_ids=tag_ids)
    
    # 验证结果
    assert isinstance(result, DataSetList)
    assert len(result.data) == 1
    assert result.total == 1
    assert result.has_more is False
    
    # 验证调用了正确的API路径和参数
    mock_admin_client.get.assert_called_once_with(
        "/datasets", 
        params={"page": 1, "limit": 30, "include_all": "false", "tag_ids": "test_tag_id_1,test_tag_id_2"}
    )


@pytest.mark.asyncio
async def test_find_list_include_all():
    """测试find_list方法，包含所有知识库"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟响应数据
    mock_response = {
        "data": [
            {
                "id": "test_dataset_id_1",
                "name": "测试知识库1",
                "description": "这是测试知识库1的描述",
                "permission": "only_me",
                "data_source_type": "upload_file",
                "indexing_technique": "high_quality",
                "created_by": "test_user",
                "created_at": 1630000000
            },
            {
                "id": "test_dataset_id_2",
                "name": "测试知识库2",
                "description": "这是测试知识库2的描述",
                "permission": "team",
                "data_source_type": "upload_file",
                "indexing_technique": "high_quality",
                "created_by": "other_user",
                "created_at": 1630000001
            }
        ],
        "total": 2,
        "has_more": False
    }
    
    # 设置模拟方法的返回值
    mock_admin_client.get.return_value = mock_response
    
    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)
    
    # 调用find_list方法，包含所有知识库
    result = await dify_dataset.find_list(include_all=True)
    
    # 验证结果
    assert isinstance(result, DataSetList)
    assert len(result.data) == 2
    assert result.total == 2
    assert result.has_more is False
    
    # 验证调用了正确的API路径和参数
    mock_admin_client.get.assert_called_once_with(
        "/datasets", 
        params={"page": 1, "limit": 30, "include_all": "true"}
    )


@pytest.mark.asyncio
async def test_find_list_invalid_page():
    """测试find_list方法，当页码无效时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)
    
    # 调用find_list方法，应该抛出ValueError
    with pytest.raises(ValueError, match="页码不能小于1"):
        await dify_dataset.find_list(page=0)


@pytest.mark.asyncio
async def test_find_list_invalid_limit():
    """测试find_list方法，当每页数量无效时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)
    
    # 调用find_list方法，应该抛出ValueError
    with pytest.raises(ValueError, match="每页数量不能小于1"):
        await dify_dataset.find_list(limit=0)


@pytest.mark.asyncio
async def test_find_list_http_error():
    """测试find_list方法，当HTTP请求失败时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟方法抛出异常
    import httpx
    mock_admin_client.get.side_effect = httpx.HTTPStatusError(
        "400 Bad Request", 
        request=httpx.Request("GET", "http://example.com"), 
        response=httpx.Response(400)
    )
    
    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)
    
    # 调用find_list方法，应该抛出HTTPStatusError
    with pytest.raises(httpx.HTTPStatusError):
        await dify_dataset.find_list() 