"""
Dify SDK - 聊天功能示例

本示例展示如何使用chat方法与Dify应用进行对话交互
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.app import DifyApp
from dify.app.schemas import ChatPayloads, ConversationEventType
from dify.http import AdminClient, ApiClient


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
ADMIN_API_KEY = os.getenv("DIFY_ADMIN_KEY")
API_KEY = os.getenv("DIFY_API_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """演示如何使用chat方法与Dify应用进行对话交互"""
    # 初始化客户端
    admin_client = AdminClient(BASE_URL, ADMIN_API_KEY)
    api_client = ApiClient(BASE_URL, API_KEY)
    
    # 初始化DifyApp
    dify_app = DifyApp(admin_client)
    
    print("聊天功能示例")
    print("-" * 30)
    
    # 首先获取应用列表，以便获取一个有效的应用ID
    app_list = await dify_app.find_list(limit=1)
    
    if not app_list.data:
        print("未找到任何应用，请确保您的账户中有创建的应用")
        return
    
    # 获取第一个应用
    app = app_list.data[0]
    print(f"使用应用: {app.name} (ID: {app.id}, 模式: {app.mode})")
    
    print("\n1. 发起聊天对话:")
    # 创建聊天请求配置
    payloads = ChatPayloads(
        query="你好，请介绍一下自己",
        user="example-user",
        response_mode="streaming",
    )
    
    # 发送聊天请求
    print("\n开始聊天...")
    answer_text = ""
    conversation_id = None
    
    try:
        async for event in dify_app.chat(app.id, payloads):
            event_type = event.get("event")
            
            if event_type == ConversationEventType.MESSAGE:
                # 输出消息内容
                answer_text += event.get("answer", "")
                print(event.get("answer", ""), end="", flush=True)
                
            elif event_type == ConversationEventType.MESSAGE_END:
                # 消息结束
                print("\n\n聊天结束")
                
                # 输出元数据
                metadata = event.get("metadata", {})
                usage = metadata.get("usage", {})
                if usage:
                    print(f"Token 使用情况: {usage.get('total_tokens', 0)} 个")
                
                # 保存会话 ID 用于后续对话
                conversation_id = event.get("conversation_id")
                if conversation_id:
                    print(f"会话 ID: {conversation_id}")
                break
                
            elif event_type == ConversationEventType.ERROR:
                # 错误事件
                print(f"\n错误: {event.get('message', '未知错误')}")
                break
                
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        return
    
    print("\n2. 继续对话:")
    if not conversation_id:
        print("未获取到会话ID，无法继续对话")
        return
        
    try:
        # 创建新的请求配置，包含会话 ID
        next_payloads = ChatPayloads(
            query="请给我讲个笑话",
            user="example-user",
            response_mode="streaming",
            conversation_id=conversation_id,
        )
        
        print("\n继续对话...")
        answer_text = ""
        
        async for next_event in dify_app.chat(app.id, next_payloads):
            next_event_type = next_event.get("event")
            
            if next_event_type == ConversationEventType.MESSAGE:
                answer_text += next_event.get("answer", "")
                print(next_event.get("answer", ""), end="", flush=True)
                
            elif next_event_type == ConversationEventType.MESSAGE_END:
                print("\n\n对话结束")
                break
                
            elif next_event_type == ConversationEventType.ERROR:
                print(f"\n错误: {next_event.get('message', '未知错误')}")
                break
                
    except Exception as e:
        print(f"\n发生错误: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
