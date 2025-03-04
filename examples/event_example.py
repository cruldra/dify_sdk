#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
事件处理示例

本示例展示如何使用ConversationEvent联合类型处理不同类型的事件
"""

import json
import time
from typing import Dict, Any

from dify.app.schemas import (
    ConversationEventType,
    ChatMessageEvent,
    AgentMessageEvent,
    MessageEndEvent,
    ErrorEvent,
    ConversationEvent, EventContainer
)
from dify.app.utils import parse_event


def process_event(event: ConversationEvent) -> Dict[str, Any]:
    """
    处理不同类型的事件
    
    Args:
        event: 事件对象
        
    Returns:
        Dict[str, Any]: 处理结果
    """
    # 使用discriminator字段进行类型判断
    if event.event == ConversationEventType.MESSAGE:
        # 处理普通消息事件
        return {
            "type": "普通消息",
            "content": event.answer,
            "message_id": event.message_id,
        }
    elif event.event == ConversationEventType.AGENT_MESSAGE:
        # 处理Agent消息事件
        return {
            "type": "Agent消息",
            "content": event.answer,
            "message_id": event.message_id,
        }
    elif event.event == ConversationEventType.MESSAGE_END:
        # 处理消息结束事件
        return {
            "type": "消息结束",
            "message_id": event.message_id,
            "usage": event.metadata.usage.dict() if event.metadata.usage else None,
        }
    elif event.event == ConversationEventType.ERROR:
        # 处理错误事件
        return {
            "type": "错误",
            "code": event.code,
            "message": event.message,
        }
    else:
        # 处理其他类型事件
        return {
            "type": f"其他事件: {event.event}",
            "raw_data": event.model_dump(),
        }


def main():
    """主函数"""
    # 创建示例事件
    current_time = int(time.time())

    # 普通消息事件
    message_event = ChatMessageEvent(
        message_id="msg_123",
        conversation_id="conv_456",
        answer="这是一个普通消息回复",
        created_at=current_time,
    )

    # Agent消息事件
    agent_message_event = AgentMessageEvent(
        task_id="task_789",
        message_id="msg_234",
        conversation_id="conv_456",
        answer="这是一个Agent消息回复",
        created_at=current_time,
    )

    # 消息结束事件
    message_end_event = MessageEndEvent(
        task_id="task_789",
        message_id="msg_123",
        conversation_id="conv_456",
    )

    # 错误事件
    error_event = ErrorEvent(
        task_id="task_789",
        message_id="msg_123",
        status=400,
        code="invalid_request",
        message="请求参数无效",
    )

    # 创建事件容器
    container = EventContainer(
        events=[
            message_event,
            agent_message_event,
            message_end_event,
            error_event,
        ]
    )

    # 处理事件
    print("处理事件示例:")
    for event in container.events:
        result = process_event(event)
        print(f"- {json.dumps(result, ensure_ascii=False)}")

    print("\n从JSON解析事件示例:")
    # 从JSON解析事件
    json_data = {
        "event": "message",
        "message_id": "msg_345",
        "conversation_id": "conv_456",
        "answer": "从JSON解析的消息",
        "created_at": current_time,
    }

    parsed_event = parse_event(json_data)
    result = process_event(parsed_event)
    print(f"- {json.dumps(result, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
