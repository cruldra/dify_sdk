#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
停止消息生成示例

本示例展示如何使用stop_message方法停止正在生成的消息
"""

import asyncio
import os
import signal
import sys
import time
from typing import AsyncGenerator

from dify import DifyClient
from dify.app.schemas import (
    ApiKey,
    ChatPayloads,
    ConversationEvent,
    ConversationEventType,
    OperationResult,
)


# 全局变量用于存储任务ID
current_task_id = None


async def start_chat(client: DifyClient, api_key: ApiKey, user_id: str) -> AsyncGenerator[ConversationEvent, None]:
    """
    开始聊天并返回事件流
    
    Args:
        client: Dify客户端
        api_key: API密钥
        user_id: 用户ID
        
    Returns:
        AsyncGenerator[ConversationEvent, None]: 事件流
    """
    # 创建聊天请求参数
    payloads = ChatPayloads(
        inputs={},
        query="请详细介绍一下人工智能的历史和发展，包括重要的里程碑和关键人物",
        user=user_id,
        response_mode="streaming",
    )
    
    # 发送聊天请求并获取事件流
    return client.app.chat(api_key, payloads)


async def stop_message_after_delay(client: DifyClient, api_key: ApiKey, task_id: str, user_id: str, delay: float = 2.0) -> OperationResult:
    """
    延迟一段时间后停止消息生成
    
    Args:
        client: Dify客户端
        api_key: API密钥
        task_id: 任务ID
        user_id: 用户ID
        delay: 延迟时间（秒）
        
    Returns:
        OperationResult: 操作结果
    """
    # 等待指定的延迟时间
    await asyncio.sleep(delay)
    print(f"\n[系统] 停止消息生成，任务ID: {task_id}")
    
    # 调用stop_message方法停止消息生成
    return await client.app.stop_message(api_key, task_id, user_id)


async def handle_chat_events(client: DifyClient, api_key: ApiKey, user_id: str):
    """
    处理聊天事件并在适当的时候停止消息生成
    
    Args:
        client: Dify客户端
        api_key: API密钥
        user_id: 用户ID
    """
    global current_task_id
    
    # 开始聊天并获取事件流
    event_stream = start_chat(client, api_key, user_id)
    
    # 用于存储是否已经启动停止任务
    stop_task_started = False
    
    try:
        async for event in event_stream:
            # 处理不同类型的事件
            if event.event == ConversationEventType.AGENT_MESSAGE:
                # 如果是Agent消息事件，获取任务ID
                if not current_task_id and hasattr(event, "task_id"):
                    current_task_id = event.task_id
                    print(f"[系统] 获取到任务ID: {current_task_id}")
                
                # 打印消息内容
                print(event.answer, end="", flush=True)
                
                # 如果有任务ID且尚未启动停止任务，则启动停止任务
                if current_task_id and not stop_task_started:
                    stop_task_started = True
                    # 创建一个任务，在3秒后停止消息生成
                    asyncio.create_task(
                        stop_message_after_delay(client, api_key, current_task_id, user_id, 3.0)
                    )
            
            elif event.event == ConversationEventType.MESSAGE:
                # 如果是普通消息事件，打印消息内容
                print(event.answer, end="", flush=True)
            
            elif event.event == ConversationEventType.MESSAGE_END:
                # 如果是消息结束事件，打印换行和结束信息
                print("\n[系统] 消息生成完成")
                if hasattr(event, "metadata") and hasattr(event.metadata, "usage"):
                    print(f"[系统] 使用情况: {event.metadata.usage.model_dump()}")
            
            elif event.event == ConversationEventType.ERROR:
                # 如果是错误事件，打印错误信息
                print(f"\n[错误] {event.code}: {event.message}")
    
    except Exception as e:
        print(f"\n[异常] 发生错误: {str(e)}")


async def main():
    """主函数"""
    # 从环境变量获取API密钥和用户ID
    api_key_str = os.environ.get("DIFY_API_KEY", "")
    user_id = os.environ.get("USER_ID", "test_user")
    
    if not api_key_str:
        print("错误: 请设置DIFY_API_KEY环境变量")
        sys.exit(1)
    
    # 创建API密钥对象
    api_key = ApiKey(
        id="",
        type="api",
        token=api_key_str,
        last_used_at=0,
        created_at=int(time.time()),
    )
    
    # 创建Dify客户端
    client = DifyClient()
    
    # 处理聊天事件
    await handle_chat_events(client, api_key, user_id)


if __name__ == "__main__":
    # 设置信号处理，以便可以通过Ctrl+C中断程序
    def signal_handler(sig, frame):
        print("\n程序被用户中断")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # 运行主函数
    asyncio.run(main()) 