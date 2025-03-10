from .schemas import *


def parse_event(data: dict) -> ConversationEvent:
    """
    根据事件类型解析为对应的事件对象

    Args:
        data: 事件数据字典

    Returns:
        ConversationEvent: 解析后的事件对象

    Raises:
        ValueError: 当事件类型不支持时抛出
    """
    event_type = data.get("event")

    if event_type == ConversationEventType.MESSAGE:
        return ChatMessageEvent(**data)
    elif event_type == ConversationEventType.AGENT_MESSAGE:
        return AgentMessageEvent(**data)
    elif event_type == ConversationEventType.AGENT_THOUGHT:
        return AgentThoughtEvent(**data)
    elif event_type == ConversationEventType.MESSAGE_FILE:
        return MessageFileEvent(**data)
    elif event_type == ConversationEventType.MESSAGE_END:
        return MessageEndEvent(**data)
    elif event_type == ConversationEventType.TTS_MESSAGE:
        return TTSMessageEvent(**data)
    elif event_type == ConversationEventType.TTS_MESSAGE_END:
        return TTSMessageEndEvent(**data)
    elif event_type == ConversationEventType.MESSAGE_REPLACE:
        return MessageReplaceEvent(**data)
    elif event_type == ConversationEventType.ERROR:
        return ErrorEvent(**data)
    elif event_type == ConversationEventType.WORKFLOW_STARTED:
        return WorkflowStartedEvent(**data)
    elif event_type == ConversationEventType.NODE_STARTED:
        return NodeStartedEvent(**data)
    elif event_type == ConversationEventType.NODE_FINISHED:
        return NodeFinishedEvent(**data)
    elif event_type == ConversationEventType.WORKFLOW_FINISHED:
        return WorkflowFinishedEvent(**data)
    elif event_type == ConversationEventType.TEXT_CHUNK:
        return TextChunkEvent(**data)
    else:
        raise ValueError(f"不支持的事件类型: {event_type}")
