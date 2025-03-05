import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from dify.app import DifyApp
from dify.app.schemas import App, AppMode, ApiKey, RunWorkflowPayloads, ConversationEvent, ConversationEventType
from dify.app.utils import parse_event
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
def dify_app(mock_admin_client):
    """创建 DifyApp 实例"""
    app = DifyApp(mock_admin_client)
    # 模拟 create_api_client 方法
    app.admin_client.create_api_client = MagicMock(return_value=mock_api_client)
    return app


@pytest.fixture
def mock_workflow_app():
    """创建模拟的工作流应用数据"""
    return App(
        id="app-workflow-123456",
        name="测试工作流应用",
        mode=AppMode.WORKFLOW,
        description="这是一个测试工作流应用",
    )


@pytest.fixture
def mock_api_key():
    """创建模拟的 API 密钥"""
    return ApiKey(
        id="key-123456",
        token="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        type="api",
        created_at="2023-01-01T00:00:00Z",
    )


@pytest.fixture
def workflow_payloads():
    """创建工作流请求配置"""
    return RunWorkflowPayloads(
        inputs={"query": "测试工作流"},
        user="test-user",
        response_mode="streaming"
    )


@pytest.fixture
def mock_events():
    """创建模拟的事件数据"""
    return [
        {"event": "workflow:started"},
        {"event": "message:content", "content": "工作流测试内容"},
        {"event": "workflow:finished"}
    ]


@pytest.fixture
def mock_conversation_events(mock_events):
    """创建模拟的 ConversationEvent 对象"""
    return [parse_event(event) for event in mock_events]


class MockResponse:
    """模拟 httpx 响应对象"""
    
    def __init__(self, status_code=200, content=None, events=None):
        self.status_code = status_code
        self.content = content or b""
        self.events = events or [
            {"event": "workflow:started"},
            {"event": "message:content", "content": "工作流测试内容"},
            {"event": "workflow:finished"}
        ]
    
    async def aread(self):
        return self.content
    
    async def aiter_lines(self):
        """模拟行迭代器"""
        for event in self.events:
            yield f'data:{json.dumps(event)}'


@pytest.mark.asyncio
async def test_run_workflow(dify_app, mock_admin_client, mock_api_client, mock_workflow_app, mock_api_key, workflow_payloads, mock_conversation_events):
    """测试运行工作流功能"""
    # 模拟 find_by_id 方法
    dify_app.find_by_id = AsyncMock(return_value=mock_workflow_app)
    
    # 模拟 get_keys 方法
    dify_app.get_keys = AsyncMock(return_value=[mock_api_key])
    
    # 模拟 parse_event 函数
    with patch('dify.app.utils.parse_event', side_effect=lambda x: mock_conversation_events[mock_events.index(x) if x in mock_events else 0]):
        # 模拟 stream 方法
        mock_response = MockResponse()
        mock_api_client.stream = AsyncMock(return_value=mock_response)
        
        # 调用被测试的方法
        events = []
        async for event in dify_app.run(mock_workflow_app.id, workflow_payloads):
            events.append(event)
        
        # 验证结果
        assert len(events) == 3
        assert all(isinstance(event, ConversationEvent) for event in events)
        assert events[0].event == ConversationEventType.WORKFLOW_STARTED
        assert events[1].event == ConversationEventType.MESSAGE_CONTENT
        assert events[1].content == "工作流测试内容"
        assert events[2].event == ConversationEventType.WORKFLOW_FINISHED
        
        # 验证调用
        dify_app.find_by_id.assert_called_once_with(mock_workflow_app.id)
        dify_app.get_keys.assert_called_once_with(mock_workflow_app.id)
        mock_api_client.stream.assert_called_once()


@pytest.mark.asyncio
async def test_run_workflow_app_not_found(dify_app, workflow_payloads):
    """测试应用未找到的情况"""
    # 模拟 find_by_id 方法返回 None
    dify_app.find_by_id = AsyncMock(return_value=None)
    
    # 调用被测试的方法，应该抛出异常
    with pytest.raises(ValueError, match="未找到对应的应用"):
        async for _ in dify_app.run("non-existent-app", workflow_payloads):
            pass


@pytest.mark.asyncio
async def test_run_workflow_no_api_key(dify_app, mock_workflow_app, workflow_payloads):
    """测试没有 API 密钥的情况"""
    # 模拟 find_by_id 方法
    dify_app.find_by_id = AsyncMock(return_value=mock_workflow_app)
    
    # 模拟 get_keys 方法返回空列表
    dify_app.get_keys = AsyncMock(return_value=[])
    
    # 调用被测试的方法，应该抛出异常
    with pytest.raises(ValueError, match=f"应用{mock_workflow_app.name}没有API密钥"):
        async for _ in dify_app.run(mock_workflow_app.id, workflow_payloads):
            pass


@pytest.mark.asyncio
async def test_run_workflow_http_error(dify_app, mock_admin_client, mock_api_client, mock_workflow_app, mock_api_key, workflow_payloads):
    """测试 HTTP 错误的情况"""
    # 模拟 find_by_id 方法
    dify_app.find_by_id = AsyncMock(return_value=mock_workflow_app)
    
    # 模拟 get_keys 方法
    dify_app.get_keys = AsyncMock(return_value=[mock_api_key])
    
    # 模拟 stream 方法返回错误响应
    mock_response = MockResponse(status_code=400, content=b'{"error":"Bad Request"}')
    mock_api_client.stream = AsyncMock(return_value=mock_response)
    
    # 调用被测试的方法，应该抛出异常
    with pytest.raises(ValueError, match="运行工作流失败"):
        async for _ in dify_app.run(mock_workflow_app.id, workflow_payloads):
            pass 