"""
测试工作流运行示例

测试examples/app/run.py示例文件的功能
"""

import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dify.app import DifyApp
from dify.app.schemas import (
    App, 
    ApiKey, 
    DifyAppMode, 
    Pagination, 
    RunWorkflowPayloads,
    ChatMessageEvent,
    MessageEndEvent,
    ErrorEvent,
    ConversationEventType,
)
from dify.http import AdminClient


@pytest.fixture
def mock_admin_client():
    """创建模拟的AdminClient"""
    client = AsyncMock(spec=AdminClient)
    return client


@pytest.fixture
def mock_api_client():
    """创建模拟的ApiClient"""
    client = AsyncMock(spec=AdminClient)
    return client


@pytest.fixture
def dify_app(mock_admin_client, mock_api_client):
    """创建DifyApp实例"""
    app = DifyApp(mock_admin_client)
    app.admin_client.create_api_client = MagicMock(return_value=mock_api_client)
    return app


@pytest.fixture
def mock_workflow_app():
    """创建模拟的工作流应用"""
    return App(
        id="app-workflow-123456",
        name="测试工作流应用",
        mode=DifyAppMode.WORKFLOW,
        description="这是一个测试工作流应用",
        created_at="2023-01-01T00:00:00Z",
    )


@pytest.fixture
def mock_api_key():
    """创建模拟的API密钥"""
    return ApiKey(
        id="key-123456",
        token="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        type="api",
        created_at="2023-01-01T00:00:00Z",
    )


@pytest.fixture
def mock_app_list(mock_workflow_app):
    """创建模拟的应用列表"""
    return Pagination[App](
        data=[mock_workflow_app],
        has_more=False,
        limit=10,
        page=1,
        total=1,
    )


@pytest.mark.asyncio
async def test_run_example(dify_app, mock_admin_client, mock_api_client, mock_app_list, mock_api_key):
    """测试工作流运行示例"""
    # 模拟find_list方法
    dify_app.find_list = AsyncMock(return_value=mock_app_list)
    
    # 模拟get_keys方法
    dify_app.get_keys = AsyncMock(return_value=[mock_api_key])
    
    # 模拟run方法
    async def mock_run(api_key, payloads):
        # 模拟返回的事件
        events = [
            ChatMessageEvent(
                message_id="msg-123",
                answer="这是工作流的响应内容",
                created_at=1234567890,
            ),
            MessageEndEvent(
                task_id="task-123",
                message_id="msg-123",
            ),
        ]
        for event in events:
            yield event
    
    dify_app.run = mock_run
    
    # 导入示例模块
    from examples.app.run import main
    
    # 运行示例
    with patch('builtins.print') as mock_print:
        await main()
        
        # 验证调用
        dify_app.find_list.assert_called_once()
        dify_app.get_keys.assert_called_once()
        
        # 验证输出
        mock_print.assert_any_call("工作流运行示例")
        mock_print.assert_any_call("开始运行工作流...")
        mock_print.assert_any_call("事件类型:", ConversationEventType.MESSAGE)
        mock_print.assert_any_call("事件类型:", ConversationEventType.MESSAGE_END)


@pytest.mark.asyncio
async def test_run_example_no_workflow_app(dify_app):
    """测试没有工作流应用的情况"""
    # 模拟find_list方法返回空列表
    empty_app_list = Pagination[App](
        data=[],
        has_more=False,
        limit=10,
        page=1,
        total=0,
    )
    dify_app.find_list = AsyncMock(return_value=empty_app_list)
    
    # 导入示例模块
    from examples.app.run import main
    
    # 运行示例
    with patch('builtins.print') as mock_print:
        await main()
        
        # 验证调用
        dify_app.find_list.assert_called_once()
        
        # 验证输出
        mock_print.assert_any_call("工作流运行示例")
        mock_print.assert_any_call("未找到任何工作流应用，请确保您的账户中有创建的工作流应用")


@pytest.mark.asyncio
async def test_run_example_no_api_key(dify_app, mock_app_list):
    """测试没有API密钥的情况"""
    # 模拟find_list方法
    dify_app.find_list = AsyncMock(return_value=mock_app_list)
    
    # 模拟get_keys方法返回空列表
    dify_app.get_keys = AsyncMock(return_value=[])
    
    # 导入示例模块
    from examples.app.run import main
    
    # 运行示例
    with patch('builtins.print') as mock_print:
        await main()
        
        # 验证调用
        dify_app.find_list.assert_called_once()
        dify_app.get_keys.assert_called_once()
        
        # 验证输出
        mock_print.assert_any_call("工作流运行示例")
        mock_print.assert_any_call(f"应用 {mock_app_list.data[0].name} 没有API密钥，请先创建API密钥")


@pytest.mark.asyncio
async def test_run_example_error(dify_app, mock_app_list, mock_api_key):
    """测试运行工作流出错的情况"""
    # 模拟find_list方法
    dify_app.find_list = AsyncMock(return_value=mock_app_list)
    
    # 模拟get_keys方法
    dify_app.get_keys = AsyncMock(return_value=[mock_api_key])
    
    # 模拟run方法返回错误
    async def mock_run_error(api_key, payloads):
        # 模拟返回的错误事件
        yield ErrorEvent(
            task_id="task-123",
            message_id="msg-123",
            status=400,
            code="bad_request",
            message="请求参数错误",
        )
    
    dify_app.run = mock_run_error
    
    # 导入示例模块
    from examples.app.run import main
    
    # 运行示例
    with patch('builtins.print') as mock_print:
        await main()
        
        # 验证调用
        dify_app.find_list.assert_called_once()
        dify_app.get_keys.assert_called_once()
        
        # 验证输出
        mock_print.assert_any_call("工作流运行示例")
        mock_print.assert_any_call("开始运行工作流...")
        mock_print.assert_any_call("事件类型:", ConversationEventType.ERROR) 