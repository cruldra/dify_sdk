"""
测试 Dify SDK 服务模块的异步方法
"""

from typing import TYPE_CHECKING, Dict, Any
import pytest
import httpx
import pytest_asyncio
from unittest.mock import MagicMock, AsyncMock

from dify.services import AppService, DifyClient, DifyAPIException
from dify.app.schemas import App, Pagination, AppMode

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch
    from pytest_mock.plugin import MockerFixture


@pytest_asyncio.fixture
async def app_service() -> AppService:
    """创建 AppService 实例的测试夹具"""
    client = DifyClient(app_key="test_app_key", admin_key="test_admin_key")
    return AppService(client=client)


@pytest.mark.asyncio
async def test_get_apps_success(app_service: AppService, mocker: "MockerFixture") -> None:
    """测试成功获取应用列表"""
    # 模拟 httpx.AsyncClient.get 的响应
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "page": 1,
        "limit": 10,
        "total": 2,
        "has_more": False,
        "data": [
            {
                "id": "app1",
                "name": "测试应用1",
                "description": "这是测试应用1",
                "mode": "chat"
            },
            {
                "id": "app2",
                "name": "测试应用2",
                "description": "这是测试应用2",
                "mode": "completion"
            }
        ]
    }
    mock_response.raise_for_status = MagicMock()
    
    # 创建 AsyncMock 对象
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.return_value = mock_response
    
    # 使用 mocker 替换 httpx.AsyncClient
    mocker.patch("httpx.AsyncClient", return_value=mock_client)
    
    # 调用方法
    result = await app_service.get_apps(page=1, limit=10)
    
    # 验证结果
    assert isinstance(result, Pagination)
    assert result.page == 1
    assert result.limit == 10
    assert result.total == 2
    assert result.has_more is False
    assert len(result.data) == 2
    
    # 验证应用数据
    assert result.data[0].id == "app1"
    assert result.data[0].name == "测试应用1"
    assert result.data[0].mode == AppMode.CHAT
    
    assert result.data[1].id == "app2"
    assert result.data[1].name == "测试应用2"
    assert result.data[1].mode == AppMode.COMPLETION


@pytest.mark.asyncio
async def test_get_apps_with_mode_filter(app_service: AppService, mocker: "MockerFixture") -> None:
    """测试使用模式过滤获取应用列表"""
    # 模拟 httpx.AsyncClient.get 的响应
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "page": 1,
        "limit": 10,
        "total": 1,
        "has_more": False,
        "data": [
            {
                "id": "app1",
                "name": "测试应用1",
                "description": "这是测试应用1",
                "mode": "chat"
            }
        ]
    }
    mock_response.raise_for_status = MagicMock()
    
    # 创建 AsyncMock 对象
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.return_value = mock_response
    
    # 使用 mocker 替换 httpx.AsyncClient
    mocker.patch("httpx.AsyncClient", return_value=mock_client)
    
    # 调用方法，使用模式过滤
    result = await app_service.get_apps(mode=AppMode.CHAT)
    
    # 验证请求参数
    args, kwargs = mock_client.__aenter__.return_value.get.call_args
    assert kwargs["params"]["mode"] == "chat"
    
    # 验证结果
    assert len(result.data) == 1
    assert result.data[0].mode == AppMode.CHAT


@pytest.mark.asyncio
async def test_get_apps_api_error(app_service: AppService, mocker: "MockerFixture") -> None:
    """测试 API 调用失败的情况"""
    # 模拟 httpx.HTTPStatusError 异常
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    
    # 创建 AsyncMock 对象
    mock_client = AsyncMock()
    mock_get = mock_client.__aenter__.return_value.get
    mock_get.side_effect = httpx.HTTPStatusError("401 Client Error", request=MagicMock(), response=mock_response)
    
    # 使用 mocker 替换 httpx.AsyncClient
    mocker.patch("httpx.AsyncClient", return_value=mock_client)
    
    # 验证异常抛出
    with pytest.raises(DifyAPIException) as excinfo:
        await app_service.get_apps()
    
    # 验证异常信息
    assert excinfo.value.status_code == 401
    assert "Unauthorized" in excinfo.value.detail 