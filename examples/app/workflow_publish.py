#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
获取工作流发布详情示例

此示例展示如何使用DifyWorkflow.get_publish方法获取工作流发布详情。
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dify.app.workflow import DifyWorkflow
from dify.http import AdminClient

API_KEY = os.getenv("DIFY_ADMIN_KEY")
BASE_URL = os.getenv("DIFY_BASE_URL")


async def main():
    """主函数"""
    # 从环境变量获取API密钥和基础URL
    app_id = "bf16d1d2-f960-4841-83f8-1aa2e654b866"

    # 创建AdminClient实例
    admin_client = AdminClient(BASE_URL, API_KEY)

    # 创建DifyWorkflow实例
    workflow = DifyWorkflow(admin_client)

    try:
        # 获取工作流发布详情
        publish = await workflow.get_publish(app_id)

        # 打印工作流ID
        print(f"工作流ID: {publish.id}")

        # 打印节点数量
        print(f"节点数量: {len(publish.graph.nodes)}")

        # 打印边数量
        print(f"边数量: {len(publish.graph.edges)}")

        # 如果有节点，打印第一个节点的信息
        if publish.graph.nodes:
            print("\n第一个节点信息:")
            node = publish.graph.nodes[0]
            print(f"  ID: {node.id}")
            print(f"  类型: {node.type}")
            if node.data and node.data.title:
                print(f"  标题: {node.data.title}")

        # 如果有边，打印第一个边的信息
        if publish.graph.edges:
            print("\n第一个边信息:")
            edge = publish.graph.edges[0]
            print(f"  ID: {edge.id}")
            print(f"  源节点: {edge.source}")
            print(f"  目标节点: {edge.target}")

    except ValueError as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"请求失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())
