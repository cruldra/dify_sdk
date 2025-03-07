import asyncio
import pytest
from unittest.mock import AsyncMock, patch

from dify.app import DifyApp
from dify.app.schemas import App, AppMode
from dify.http import AdminClient


@pytest.fixture
def mock_admin_client():
    """创建模拟的 AdminClient"""
    client = AsyncMock(spec=AdminClient)
    return client


@pytest.fixture
def dify_app(mock_admin_client):
    """创建 DifyApp 实例"""
    return DifyApp(mock_admin_client)


@pytest.fixture
def mock_app_response():
    """创建模拟的应用响应数据"""
    return {
        "id": "app-123456",
        "name": "测试应用",
        "mode": "chat",
        "description": "这是一个测试应用",
        "icon_type": "emoji",
        "icon": "🤖",
        "icon_background": "#FFEAD5",
        "created_at": 1646092800000,
        "updated_at": 1646092800000
    }


@pytest.mark.asyncio
async def test_create_app(dify_app, mock_admin_client, mock_app_response):
    """测试创建应用功能"""
    # 设置模拟响应
    mock_admin_client.post.return_value = mock_app_response
    
    # 调用创建应用方法
    app = await dify_app.create(
        name="测试应用",
        mode=AppMode.CHAT,
        description="这是一个测试应用",
        icon_type="emoji",
        icon="🤖",
        icon_background="#FFEAD5"
    )
    
    # 验证结果
    assert isinstance(app, App)
    assert app.id == "app-123456"
    assert app.name == "测试应用"
    assert app.mode == AppMode.CHAT
    assert app.description == "这是一个测试应用"
    assert app.icon_type == "emoji"
    assert app.icon == "🤖"
    assert app.icon_background == "#FFEAD5"
    
    # 验证调用
    mock_admin_client.post.assert_called_once_with(
        "/apps",
        json={
            "name": "测试应用",
            "mode": "chat",
            "description": "这是一个测试应用",
            "icon_type": "emoji",
            "icon": "🤖",
            "icon_background": "#FFEAD5"
        }
    )


@pytest.mark.asyncio
async def test_create_app_with_empty_name(dify_app):
    """测试创建应用时名称为空的情况"""
    with pytest.raises(ValueError, match="应用名称不能为空"):
        await dify_app.create(
            name="",
            mode=AppMode.CHAT
        )


@pytest.mark.asyncio
async def test_create_app_with_empty_mode(dify_app):
    """测试创建应用时模式为空的情况"""
    with pytest.raises(ValueError, match="应用模式不能为空"):
        await dify_app.create(
            name="测试应用",
            mode=None
        )


@pytest.mark.asyncio
async def test_create_app_with_string_mode(dify_app, mock_admin_client, mock_app_response):
    """测试使用字符串模式创建应用"""
    # 设置模拟响应
    mock_admin_client.post.return_value = mock_app_response
    
    # 调用创建应用方法，使用字符串模式
    app = await dify_app.create(
        name="测试应用",
        mode="chat",
        description="这是一个测试应用"
    )
    
    # 验证结果
    assert isinstance(app, App)
    assert app.mode == AppMode.CHAT
    
    # 验证调用
    mock_admin_client.post.assert_called_once_with(
        "/apps",
        json={
            "name": "测试应用",
            "mode": "chat",
            "description": "这是一个测试应用",
            "icon_type": "emoji",
            "icon": "🤖",
            "icon_background": "#FFEAD5"
        }
    ) 