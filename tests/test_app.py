import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from dify.app import DifyApp
from dify.app.schemas import App, DifyAppMode, ChatPayloads
from dify.http import AdminClient, ApiClient


@pytest.fixture
def mock_admin_client():
    """创建模拟的 AdminClient"""
    client = AsyncMock(spec=AdminClient)
    return client


@pytest.fixture
def mock_api_client():
    """创建模拟的 ApiClient"""
    client = AsyncMock(spec=ApiClient)
    return client


@pytest.fixture
def dify_app(mock_admin_client, mock_api_client):
    """创建 DifyApp 实例"""
    return DifyApp(mock_admin_client, mock_api_client)


@pytest.fixture
def mock_app():
    """创建模拟的应用数据"""
    return {
        "id": "app-123456",
        "name": "测试应用",
        "mode": DifyAppMode.CHAT,
        "description": "这是一个测试应用",
    }


@pytest.fixture
def chat_payloads():
    """创建聊天请求配置"""
    return ChatPayloads(
        query="Hello",
        user="test-user",
        response_mode="streaming"
    )


@pytest.mark.asyncio
async def test_find_by_id(dify_app, mock_admin_client, mock_app):
    """测试 find_by_id 方法"""
    # 设置模拟返回值
    mock_admin_client.get.return_value = mock_app
    
    # 调用方法
    app = await dify_app.find_by_id("app-123456")
    
    # 验证结果
    assert isinstance(app, App)
    assert app.id == "app-123456"
    assert app.name == "测试应用"
    assert app.mode == DifyAppMode.CHAT
    
    # 验证调用
    mock_admin_client.get.assert_called_once_with("/apps/app-123456")


@pytest.mark.asyncio
async def test_chat(dify_app, mock_api_client, chat_payloads):
    """测试 chat 方法"""
    # 模拟流式响应
    async def mock_stream(*args, **kwargs):
        # 模拟返回的事件数据
        events = [
            b'data: {"event": "message", "message_id": "msg-123", "answer": "Hello"}\n',
            b'data: {"event": "message_end", "message_id": "msg-123"}\n'
        ]
        for event in events:
            yield event
    
    # 设置模拟返回值
    mock_api_client.stream.return_value = mock_stream()
    
    # 调用方法并收集结果
    results = []
    async for event in dify_app.chat("app-123456", chat_payloads):
        results.append(event)
    
    # 验证结果
    assert len(results) == 2
    assert results[0]["event"] == "message"
    assert results[0]["answer"] == "Hello"
    assert results[1]["event"] == "message_end"
    
    # 验证调用
    mock_api_client.stream.assert_called_once()
    args, kwargs = mock_api_client.stream.call_args
    assert args[0] == "/chat-messages"
    assert kwargs["method"] == "POST"
    assert kwargs["json"]["query"] == "Hello"


@pytest.mark.asyncio
async def test_completion(dify_app, mock_api_client, chat_payloads):
    """测试 completion 方法"""
    # 模拟流式响应
    async def mock_stream(*args, **kwargs):
        # 模拟返回的事件数据
        events = [
            b'data: {"event": "message", "message_id": "msg-123", "answer": "This is a completion"}\n',
            b'data: {"event": "message_end", "message_id": "msg-123"}\n'
        ]
        for event in events:
            yield event
    
    # 设置模拟返回值
    mock_api_client.stream.return_value = mock_stream()
    
    # 调用方法并收集结果
    results = []
    async for event in dify_app.completion("app-123456", chat_payloads):
        results.append(event)
    
    # 验证结果
    assert len(results) == 2
    assert results[0]["event"] == "message"
    assert results[0]["answer"] == "This is a completion"
    assert results[1]["event"] == "message_end"
    
    # 验证调用
    mock_api_client.stream.assert_called_once()
    args, kwargs = mock_api_client.stream.call_args
    assert args[0] == "/completion-messages"
    assert kwargs["method"] == "POST"
    assert kwargs["json"]["query"] == "Hello"


@pytest.mark.asyncio
async def test_run(dify_app, mock_api_client, chat_payloads):
    """测试 run 方法"""
    # 模拟流式响应
    async def mock_stream(*args, **kwargs):
        # 模拟返回的事件数据
        events = [
            b'data: {"event": "message", "message_id": "msg-123", "answer": "Workflow result"}\n',
            b'data: {"event": "message_end", "message_id": "msg-123"}\n'
        ]
        for event in events:
            yield event
    
    # 设置模拟返回值
    mock_api_client.stream.return_value = mock_stream()
    
    # 调用方法并收集结果
    results = []
    async for event in dify_app.run("app-123456", chat_payloads):
        results.append(event)
    
    # 验证结果
    assert len(results) == 2
    assert results[0]["event"] == "message"
    assert results[0]["answer"] == "Workflow result"
    assert results[1]["event"] == "message_end"
    
    # 验证调用
    mock_api_client.stream.assert_called_once()
    args, kwargs = mock_api_client.stream.call_args
    assert args[0] == "/workflow-executions"
    assert kwargs["method"] == "POST"
    assert kwargs["json"]["query"] == "Hello"


@pytest.mark.asyncio
async def test_chat_with_error(dify_app, mock_api_client, chat_payloads):
    """测试 chat 方法的错误处理"""
    # 模拟 HTTP 错误
    error_response = MagicMock()
    error_response.status_code = 400
    error_response.aread = AsyncMock(return_value=b'{"error": "Bad Request"}')
    
    # 设置模拟异常
    mock_api_client.stream.side_effect = Exception("模拟异常")
    
    # 调用方法并验证异常
    with pytest.raises(ValueError) as excinfo:
        async for _ in dify_app.chat("app-123456", chat_payloads):
            pass
    
    # 验证异常信息
    assert "发送消息时发生错误" in str(excinfo.value) 