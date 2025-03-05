#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试重命名对话功能
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from dify.app import DifyApp
from dify.app.schemas import ApiKey
from dify.app.conversation.schemas import Conversation, ConversationRenamePayloads
from dify.http import AdminClient


@pytest.mark.asyncio
async def test_rename_conversation(mocker):
    """测试重命名对话功能"""
    # 模拟API密钥
    api_key = ApiKey(id="test-key-id", type="api", token="test-token")
    
    # 模拟会话ID和用户ID
    conversation_id = "test-conversation-id"
    user_id = "test-user-id"
    new_name = "新对话名称"
    
    # 模拟重命名请求参数
    rename_payloads = ConversationRenamePayloads(
        name=new_name,
        auto_generate=False,
        user=user_id
    )
    
    # 模拟重命名响应
    mock_response = {
        "id": conversation_id,
        "name": new_name,
        "inputs": {},
        "status": "normal",
        "introduction": "这是一个测试对话",
        "created_at": 1625097600,
        "updated_at": 1625097600
    }
    
    # 模拟AdminClient
    admin_client = MagicMock(spec=AdminClient)
    
    # 模拟API客户端
    mock_api_client = AsyncMock()
    mock_api_client.post = AsyncMock(return_value=mock_response)
    
    # 模拟create_api_client方法
    admin_client.create_api_client = MagicMock(return_value=mock_api_client)
    
    # 创建DifyApp实例
    dify_app = DifyApp(admin_client)
    
    # 调用rename方法
    result = await dify_app.conversation.rename(api_key, conversation_id, rename_payloads)
    
    # 验证结果
    assert isinstance(result, Conversation)
    assert result.id == conversation_id
    assert result.name == new_name
    
    # 验证方法调用
    admin_client.create_api_client.assert_called_once_with(api_key.token)
    mock_api_client.post.assert_called_once_with(
        f"/conversations/{conversation_id}/name",
        json=rename_payloads.model_dump(exclude_none=True),
    )


@pytest.mark.asyncio
async def test_rename_conversation_auto_generate(mocker):
    """测试自动生成对话名称功能"""
    # 模拟API密钥
    api_key = ApiKey(id="test-key-id", type="api", token="test-token")
    
    # 模拟会话ID和用户ID
    conversation_id = "test-conversation-id"
    user_id = "test-user-id"
    auto_generated_name = "自动生成的对话名称"
    
    # 模拟重命名请求参数
    rename_payloads = ConversationRenamePayloads(
        auto_generate=True,
        user=user_id
    )
    
    # 模拟重命名响应
    mock_response = {
        "id": conversation_id,
        "name": auto_generated_name,
        "inputs": {},
        "status": "normal",
        "introduction": "这是一个测试对话",
        "created_at": 1625097600,
        "updated_at": 1625097600
    }
    
    # 模拟AdminClient
    admin_client = MagicMock(spec=AdminClient)
    
    # 模拟API客户端
    mock_api_client = AsyncMock()
    mock_api_client.post = AsyncMock(return_value=mock_response)
    
    # 模拟create_api_client方法
    admin_client.create_api_client = MagicMock(return_value=mock_api_client)
    
    # 创建DifyApp实例
    dify_app = DifyApp(admin_client)
    
    # 调用rename方法
    result = await dify_app.conversation.rename(api_key, conversation_id, rename_payloads)
    
    # 验证结果
    assert isinstance(result, Conversation)
    assert result.id == conversation_id
    assert result.name == auto_generated_name
    
    # 验证方法调用
    admin_client.create_api_client.assert_called_once_with(api_key.token)
    mock_api_client.post.assert_called_once_with(
        f"/conversations/{conversation_id}/name",
        json=rename_payloads.model_dump(exclude_none=True),
    )


@pytest.mark.asyncio
async def test_rename_conversation_with_empty_api_key():
    """测试使用空API密钥重命名对话时抛出异常"""
    # 模拟AdminClient
    admin_client = MagicMock(spec=AdminClient)
    
    # 创建DifyApp实例
    dify_app = DifyApp(admin_client)
    
    # 模拟重命名请求参数
    rename_payloads = ConversationRenamePayloads(
        name="新名称",
        user="test-user-id"
    )
    
    # 调用rename方法，应该抛出ValueError
    with pytest.raises(ValueError, match="API密钥不能为空"):
        await dify_app.conversation.rename(None, "test-conversation-id", rename_payloads)


@pytest.mark.asyncio
async def test_rename_conversation_with_empty_conversation_id():
    """测试使用空会话ID重命名对话时抛出异常"""
    # 模拟API密钥
    api_key = ApiKey(id="test-key-id", type="api", token="test-token")
    
    # 模拟AdminClient
    admin_client = MagicMock(spec=AdminClient)
    
    # 创建DifyApp实例
    dify_app = DifyApp(admin_client)
    
    # 模拟重命名请求参数
    rename_payloads = ConversationRenamePayloads(
        name="新名称",
        user="test-user-id"
    )
    
    # 调用rename方法，应该抛出ValueError
    with pytest.raises(ValueError, match="会话ID不能为空"):
        await dify_app.conversation.rename(api_key, "", rename_payloads) 