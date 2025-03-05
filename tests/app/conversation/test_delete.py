#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试删除对话功能
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from dify.app import DifyApp
from dify.app.schemas import ApiKey, OperationResult
from dify.http import AdminClient


@pytest.mark.asyncio
async def test_delete_conversation(mocker):
    """测试删除对话功能"""
    # 模拟API密钥
    api_key = ApiKey(id="test-key-id", type="api", token="test-token")
    
    # 模拟会话ID和用户ID
    conversation_id = "test-conversation-id"
    user_id = "test-user-id"
    
    # 模拟AdminClient
    admin_client = MagicMock(spec=AdminClient)
    
    # 模拟API客户端
    mock_api_client = AsyncMock()
    mock_api_client.delete = AsyncMock(return_value=None)
    
    # 模拟create_api_client方法
    admin_client.create_api_client = MagicMock(return_value=mock_api_client)
    
    # 创建DifyApp实例
    dify_app = DifyApp(admin_client)
    
    # 调用delete方法
    result = await dify_app.conversation.delete(api_key, conversation_id, user_id)
    
    # 验证结果
    assert isinstance(result, OperationResult)
    assert result.result == "success"
    
    # 验证方法调用
    admin_client.create_api_client.assert_called_once_with(api_key.token)
    mock_api_client.delete.assert_called_once_with(
        f"/conversations/{conversation_id}",
        params={"user": user_id},
    )


@pytest.mark.asyncio
async def test_delete_conversation_with_empty_api_key():
    """测试使用空API密钥删除对话时抛出异常"""
    # 模拟AdminClient
    admin_client = MagicMock(spec=AdminClient)
    
    # 创建DifyApp实例
    dify_app = DifyApp(admin_client)
    
    # 调用delete方法，应该抛出ValueError
    with pytest.raises(ValueError, match="API密钥不能为空"):
        await dify_app.conversation.delete(None, "test-conversation-id", "test-user-id")


@pytest.mark.asyncio
async def test_delete_conversation_with_empty_conversation_id():
    """测试使用空会话ID删除对话时抛出异常"""
    # 模拟API密钥
    api_key = ApiKey(id="test-key-id", type="api", token="test-token")
    
    # 模拟AdminClient
    admin_client = MagicMock(spec=AdminClient)
    
    # 创建DifyApp实例
    dify_app = DifyApp(admin_client)
    
    # 调用delete方法，应该抛出ValueError
    with pytest.raises(ValueError, match="会话ID不能为空"):
        await dify_app.conversation.delete(api_key, "", "test-user-id")


@pytest.mark.asyncio
async def test_delete_conversation_with_empty_user_id():
    """测试使用空用户ID删除对话时抛出异常"""
    # 模拟API密钥
    api_key = ApiKey(id="test-key-id", type="api", token="test-token")
    
    # 模拟AdminClient
    admin_client = MagicMock(spec=AdminClient)
    
    # 创建DifyApp实例
    dify_app = DifyApp(admin_client)
    
    # 调用delete方法，应该抛出ValueError
    with pytest.raises(ValueError, match="用户ID不能为空"):
        await dify_app.conversation.delete(api_key, "test-conversation-id", "") 