#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试补全功能

测试DifyApp.completion方法的功能
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from dify.app import DifyApp
from dify.app.schemas import ApiKey, ChatPayloads, ChatMessageEvent, MessageEndEvent
from dify.http import AdminClient


@pytest.fixture
def mock_admin_client():
    """创建模拟的AdminClient"""
    client = MagicMock(spec=AdminClient)
    client.create_api_client = MagicMock()
    return client


@pytest.fixture
def mock_api_key():
    """创建模拟的API密钥"""
    return ApiKey(
        id="key-123456",
        token="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        type="api",
        created_at=1677649200,
    )


@pytest.fixture
def mock_api_client():
    """创建模拟的API客户端"""
    client = AsyncMock()
    return client


@pytest.fixture
def completion_payloads():
    """创建补全请求配置"""
    return ChatPayloads(
        inputs={"text": "北京是中国的首都，上海是"},
        user="test-user",
        response_mode="streaming",
    )


class TestCompletion:
    """测试补全功能类"""

    @pytest.mark.asyncio
    async def test_completion_success(
        self, mock_admin_client, mock_api_key, mock_api_client, completion_payloads
    ):
        """测试补全功能成功场景"""
        # 设置模拟响应
        mock_admin_client.create_api_client.return_value = mock_api_client

        # 模拟流式响应
        message_event = ChatMessageEvent(
            message_id="msg-123",
            answer="中国的经济中心",
            created_at=1677649200,
        )
        end_event = MessageEndEvent(
            task_id="task-123",
            message_id="msg-123",
        )

        # 将事件转换为流式响应格式
        message_data = f"data:{json.dumps(message_event.model_dump())}\n"
        end_data = f"data:{json.dumps(end_event.model_dump())}\n"

        # 设置模拟流式响应
        mock_api_client.stream.return_value.__aiter__.return_value = [
            message_data.encode("utf-8"),
            end_data.encode("utf-8"),
        ]

        # 创建DifyApp实例
        dify_app = DifyApp(mock_admin_client)

        # 调用completion方法
        events = []
        async for event in dify_app.completion(mock_api_key, completion_payloads):
            events.append(event)

        # 验证结果
        assert len(events) == 2
        assert events[0].event == "message"
        assert events[0].answer == "中国的经济中心"
        assert events[1].event == "message_end"

        # 验证API客户端调用
        mock_admin_client.create_api_client.assert_called_once_with(mock_api_key.token)
        mock_api_client.stream.assert_called_once()
        call_args = mock_api_client.stream.call_args[1]
        assert call_args["json"] == completion_payloads.model_dump(exclude_none=True)

    @pytest.mark.asyncio
    async def test_completion_empty_api_key(self, mock_admin_client, completion_payloads):
        """测试API密钥为空的场景"""
        # 创建DifyApp实例
        dify_app = DifyApp(mock_admin_client)

        # 调用completion方法，应该抛出ValueError
        with pytest.raises(ValueError) as excinfo:
            async for _ in dify_app.completion(None, completion_payloads):
                pass

        # 验证错误消息
        assert "API密钥不能为空" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_completion_empty_query_and_inputs(
        self, mock_admin_client, mock_api_key
    ):
        """测试查询和输入都为空的场景"""
        # 创建DifyApp实例
        dify_app = DifyApp(mock_admin_client)

        # 创建空的请求配置
        empty_payloads = ChatPayloads(
            query=None,
            inputs={},
            user="test-user",
        )

        # 调用completion方法，应该抛出ValueError
        with pytest.raises(ValueError) as excinfo:
            async for _ in dify_app.completion(mock_api_key, empty_payloads):
                pass

        # 验证错误消息
        assert "消息内容和inputs不能同时为空" in str(excinfo.value) 