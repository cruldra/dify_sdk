import pytest
from unittest.mock import AsyncMock, patch

from dify.app.conversation import DifyConversation, MessageFeedbackPayloads
from dify.app.schemas import ApiKey, OperationResult
from dify.http import AdminClient


@pytest.fixture
def admin_client():
    return AsyncMock(spec=AdminClient)


@pytest.fixture
def conversation_service(admin_client):
    return DifyConversation(admin_client)


@pytest.fixture
def api_key():
    return ApiKey(token="test_api_key")


@pytest.fixture
def message_id():
    return "test_message_id"


@pytest.fixture
def feedback_payloads():
    return MessageFeedbackPayloads(
        rating="like",
        user="test_user",
        content="测试反馈内容",
    )


@pytest.mark.asyncio
async def test_submit_feedback_success(
    conversation_service, api_key, message_id, feedback_payloads
):
    # 模拟API客户端
    api_client_mock = AsyncMock()
    conversation_service.admin_client.create_api_client.return_value = api_client_mock
    
    # 模拟API响应
    api_client_mock.post.return_value = {"result": "success"}
    
    # 调用方法
    result = await conversation_service.submit_feedback(
        api_key=api_key,
        message_id=message_id,
        payloads=feedback_payloads,
    )
    
    # 验证结果
    assert isinstance(result, OperationResult)
    assert result.result == "success"
    
    # 验证API调用
    conversation_service.admin_client.create_api_client.assert_called_once_with(api_key.token)
    api_client_mock.post.assert_called_once_with(
        f"/messages/{message_id}/feedbacks",
        json=feedback_payloads.model_dump(exclude_none=True),
    )


@pytest.mark.asyncio
async def test_submit_feedback_empty_api_key(conversation_service, message_id, feedback_payloads):
    # 测试空API密钥
    with pytest.raises(ValueError, match="API密钥不能为空"):
        await conversation_service.submit_feedback(
            api_key=None,
            message_id=message_id,
            payloads=feedback_payloads,
        )


@pytest.mark.asyncio
async def test_submit_feedback_empty_message_id(conversation_service, api_key, feedback_payloads):
    # 测试空消息ID
    with pytest.raises(ValueError, match="消息ID不能为空"):
        await conversation_service.submit_feedback(
            api_key=api_key,
            message_id="",
            payloads=feedback_payloads,
        )


@pytest.mark.asyncio
async def test_submit_feedback_http_error(
    conversation_service, api_key, message_id, feedback_payloads
):
    # 模拟API客户端
    api_client_mock = AsyncMock()
    conversation_service.admin_client.create_api_client.return_value = api_client_mock
    
    # 模拟HTTP错误
    import httpx
    error = httpx.HTTPStatusError(
        "Error", request=AsyncMock(), response=AsyncMock()
    )
    api_client_mock.post.side_effect = error
    
    # 测试HTTP错误传播
    with pytest.raises(httpx.HTTPStatusError):
        await conversation_service.submit_feedback(
            api_key=api_key,
            message_id=message_id,
            payloads=feedback_payloads,
        ) 