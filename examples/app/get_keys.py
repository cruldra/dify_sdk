"""
Dify SDK - 获取API密钥列表示例

本示例展示如何使用get_keys方法获取Dify应用的API密钥列表
"""

import asyncio
import os
from dotenv import load_dotenv

from dify.http import AdminClient
from dify.app import DifyApp


# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥和基础URL
API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")
# 从环境变量获取应用ID，或者使用默认值
APP_ID = os.getenv("DIFY_APP_ID", "96b8d447-293a-401c-bb7f-f9b16f9ee09b")

async def main():
    """演示如何使用get_keys方法获取Dify应用的API密钥列表"""
    # 初始化AdminClient
    admin_client = AdminClient(BASE_URL, API_KEY)
    
    # 初始化DifyApp
    dify_app = DifyApp(admin_client)
    
    print("获取API密钥列表示例")
    print("-" * 30)
    
    # 确保APP_ID已设置
    if APP_ID == "your-app-id-here":
        print("请设置DIFY_APP_ID环境变量或在代码中直接指定应用ID")
        return
    
    # 获取应用详情
    try:
        app = await dify_app.find_by_id(APP_ID)
        print(f"应用名称: {app.name}")
        print(f"应用ID: {app.id}")
        print(f"应用模式: {app.mode}")
        print()
    except Exception as e:
        print(f"获取应用详情失败: {e}")
        return
    
    # 获取API密钥列表
    print("获取API密钥列表:")
    try:
        api_keys = await dify_app.get_keys(APP_ID)
        
        if not api_keys:
            print("  该应用暂无API密钥")
        else:
            print(f"  找到 {len(api_keys)} 个API密钥:")
            
            for i, key in enumerate(api_keys, 1):
                print(f"  {i}. API密钥详情:")
                print(f"     ID: {key.id}")
                print(f"     类型: {key.type}")
                # 注意：token通常只在创建时返回，这里可能为None
                if hasattr(key, 'token') and key.token:
                    print(f"     令牌: {key.token}")
                if key.last_used_at:
                    print(f"     最后使用时间: {key.last_used_at}")
                print(f"     创建时间: {key.created_at}")
                print()
                
    except Exception as e:
        print(f"获取API密钥列表失败: {e}")
    
    # 创建新的API密钥示例
    print("\n创建新的API密钥:")
    try:
        new_key = await dify_app.create_api_key(APP_ID)
        print("  新API密钥创建成功:")
        print(f"  ID: {new_key.id}")
        print(f"  类型: {new_key.type}")
        print(f"  令牌: {new_key.token}")
        print(f"  创建时间: {new_key.created_at}")
        print("\n  注意: 请妥善保存上述API密钥，它只会显示一次！")
        
        # 再次获取API密钥列表，验证新密钥已添加
        print("\n再次获取API密钥列表，验证新密钥已添加:")
        updated_keys = await dify_app.get_keys(APP_ID)
        print(f"  现在共有 {len(updated_keys)} 个API密钥")
        
    except Exception as e:
        print(f"创建新API密钥失败: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 