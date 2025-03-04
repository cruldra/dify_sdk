#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试事件模式

测试ConversationEvent联合类型的功能
"""

import time

import pytest

from dify.app.schemas import (
    ConversationEventType,
    EventContainer,
    ChatMessageEvent,
    AgentMessageEvent,
    ErrorEvent,
)
from dify.app.utils import parse_event


class TestEventSchemas:
    """测试事件模式类"""

    def setup_method(self):
        """测试前准备"""
        self.current_time = int(time.time())

    def test_chat_message_event(self):
        """测试聊天消息事件"""
        # 创建事件
        event = ChatMessageEvent(
            message_id="msg_123",
            conversation_id="conv_456",
            answer="这是一个测试消息",
            created_at=self.current_time,
        )

        # 验证事件类型
        assert event.event == ConversationEventType.MESSAGE
        assert event.message_id == "msg_123"
        assert event.conversation_id == "conv_456"
        assert event.answer == "这是一个测试消息"
        assert event.created_at == self.current_time

        # 序列化和反序列化
        json_data = event.model_dump()
        parsed_event = parse_event(json_data)
        assert isinstance(parsed_event, ChatMessageEvent)
        assert parsed_event.event == ConversationEventType.MESSAGE
        assert parsed_event.message_id == "msg_123"

    def test_agent_message_event(self):
        """测试Agent消息事件"""
        # 创建事件
        event = AgentMessageEvent(
            task_id="task_789",
            message_id="msg_234",
            conversation_id="conv_456",
            answer="这是一个Agent测试消息",
            created_at=self.current_time,
        )

        # 验证事件类型
        assert event.event == ConversationEventType.AGENT_MESSAGE
        assert event.task_id == "task_789"
        assert event.message_id == "msg_234"
        assert event.conversation_id == "conv_456"
        assert event.answer == "这是一个Agent测试消息"
        assert event.created_at == self.current_time

        # 序列化和反序列化
        json_data = event.model_dump()
        parsed_event = parse_event(json_data)
        assert isinstance(parsed_event, AgentMessageEvent)
        assert parsed_event.event == ConversationEventType.AGENT_MESSAGE
        assert parsed_event.task_id == "task_789"

    def test_error_event(self):
        """测试错误事件"""
        # 创建事件
        event = ErrorEvent(
            task_id="task_789",
            message_id="msg_123",
            status=400,
            code="invalid_request",
            message="请求参数无效",
        )

        # 验证事件类型
        assert event.event == ConversationEventType.ERROR
        assert event.task_id == "task_789"
        assert event.message_id == "msg_123"
        assert event.status == 400
        assert event.code == "invalid_request"
        assert event.message == "请求参数无效"

        # 序列化和反序列化
        json_data = event.model_dump()
        parsed_event = parse_event(json_data)
        assert isinstance(parsed_event, ErrorEvent)
        assert parsed_event.event == ConversationEventType.ERROR
        assert parsed_event.code == "invalid_request"

    def test_event_container(self):
        """测试事件容器"""
        # 创建事件
        message_event = ChatMessageEvent(
            message_id="msg_123",
            conversation_id="conv_456",
            answer="这是一个普通消息回复",
            created_at=self.current_time,
        )

        error_event = ErrorEvent(
            task_id="task_789",
            message_id="msg_123",
            status=400,
            code="invalid_request",
            message="请求参数无效",
        )

        # 创建容器
        container = EventContainer(
            events=[message_event, error_event]
        )

        # 验证容器
        assert len(container.events) == 2
        assert isinstance(container.events[0], ChatMessageEvent)
        assert isinstance(container.events[1], ErrorEvent)

        # 序列化和反序列化
        json_data = container.model_dump()
        assert len(json_data["events"]) == 2
        assert json_data["events"][0]["event"] == ConversationEventType.MESSAGE
        assert json_data["events"][1]["event"] == ConversationEventType.ERROR

    def test_parse_event_invalid_type(self):
        """测试解析无效事件类型"""
        # 创建无效事件数据
        json_data = {
            "event": "invalid_event_type",
            "message_id": "msg_123",
        }

        # 验证解析异常
        with pytest.raises(ValueError) as excinfo:
            parse_event(json_data)

        assert "不支持的事件类型" in str(excinfo.value)
