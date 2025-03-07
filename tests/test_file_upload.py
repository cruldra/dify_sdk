"""
测试文件上传功能
"""

import os
import tempfile
import pytest
from unittest.mock import AsyncMock, patch, mock_open

from dify.file import DifyFile
from dify.file.schemas import DifyFile


@pytest.mark.asyncio
async def test_upload():
    """测试upload方法"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟响应数据
    mock_response = {
        "id": "test_file_id",
        "name": "test.txt",
        "size": 100,
        "extension": "txt",
        "mime_type": "text/plain",
        "created_by": "test_user",
        "created_at": 1630000000
    }
    
    # 设置模拟方法的返回值
    mock_admin_client.upload.return_value = mock_response
    
    # 创建DifyFile实例
    dify_file = DifyFile(mock_admin_client)
    
    # 创建临时文件用于测试
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"Test content")
        temp_file_path = temp_file.name
    
    try:
        # 调用upload方法
        result = await dify_file.upload(temp_file_path)
        
        # 验证结果
        assert isinstance(result, DifyFile)
        assert result.id == "test_file_id"
        assert result.name == "test.txt"
        assert result.size == 100
        assert result.extension == "txt"
        assert result.mime_type == "text/plain"
        
        # 验证调用了正确的API路径和参数
        mock_admin_client.upload.assert_called_once()
        call_args = mock_admin_client.upload.call_args
        assert call_args[0][0] == "/files/upload?source=datasets"
        
        # 验证文件参数
        files_arg = call_args[1]["files"]
        assert "file" in files_arg
        assert os.path.basename(temp_file_path) == files_arg["file"][0]
        
    finally:
        # 清理临时文件
        os.unlink(temp_file_path)


@pytest.mark.asyncio
async def test_upload_with_custom_source():
    """测试upload方法，使用自定义source"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 设置模拟响应数据
    mock_response = {
        "id": "test_file_id",
        "name": "test.txt",
        "size": 100,
        "extension": "txt",
        "mime_type": "text/plain"
    }
    
    # 设置模拟方法的返回值
    mock_admin_client.upload.return_value = mock_response
    
    # 创建DifyFile实例
    dify_file = DifyFile(mock_admin_client)
    
    # 创建临时文件用于测试
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"Test content")
        temp_file_path = temp_file.name
    
    try:
        # 调用upload方法，使用自定义source
        custom_source = "app"
        result = await dify_file.upload(temp_file_path, source=custom_source)
        
        # 验证结果
        assert isinstance(result, DifyFile)
        
        # 验证调用了正确的API路径和参数
        mock_admin_client.upload.assert_called_once()
        call_args = mock_admin_client.upload.call_args
        assert call_args[0][0] == f"/files/upload?source={custom_source}"
        
    finally:
        # 清理临时文件
        os.unlink(temp_file_path)


@pytest.mark.asyncio
async def test_upload_empty_file_path():
    """测试upload方法，当文件路径为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyFile实例
    dify_file = DifyFile(mock_admin_client)
    
    # 调用upload方法，应该抛出ValueError
    with pytest.raises(ValueError, match="文件路径不能为空"):
        await dify_file.upload("")


@pytest.mark.asyncio
async def test_upload_non_existent_file():
    """测试upload方法，当文件不存在时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()
    
    # 创建DifyFile实例
    dify_file = DifyFile(mock_admin_client)
    
    # 调用upload方法，应该抛出ValueError
    non_existent_file = "non_existent_file.txt"
    with pytest.raises(ValueError, match=f"文件不存在: {non_existent_file}"):
        await dify_file.upload(non_existent_file) 