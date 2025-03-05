#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试消息列表功能
"""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from dify.app import DifyApp
from dify.app.conversation.schemas import MessageList, MessageListQueryPayloads
from dify.schemas import ApiKey


class TestMessages(unittest.TestCase):
    """测试消息列表相关功能"""

    def setUp(self):
        """设置测试环境"""
        self.admin_client = MagicMock()
        self.app = DifyApp(self.admin_client)
        self.api_key = ApiKey(
            id="test_key_id",
            type="api",
            token="test_token",
            last_used_at=1234567890,
            created_at=1234567890,
        )
        self.api_client = AsyncMock()
        self.admin_client.create_api_client.return_value = self.api_client

    @pytest.mark.asyncio
    async def test_fetch_messages_with_valid_params(self):
        """测试使用有效参数获取消息列表"""
        # 准备测试数据
        mock_response = {
            "data": [
                {
                    "id": "msg_123",
                    "conversation_id": "conv_123",
                    "inputs": {},
                    "query": "你好，这是一个测试问题",
                    "answer": "你好，这是一个测试回答",
                    "created_at": 1234567890,
                    "feedback": {},
                    "message_files": [],
                    "agent_thoughts": [],
                    "retriever_resources": [],
                },
                {
                    "id": "msg_456",
                    "conversation_id": "conv_123",
                    "inputs": {},
                    "query": "第二个测试问题",
                    "answer": "第二个测试回答",
                    "created_at": 1234567891,
                    "feedback": {},
                    "message_files": [],
                    "agent_thoughts": [],
                    "retriever_resources": [],
                },
            ],
            "has_more": False,
            "limit": 20,
        }

        # 设置模拟返回值
        self.api_client.get.return_value = mock_response

        # 创建查询参数
        query_params = MessageListQueryPayloads(
            conversation_id="conv_123",
            user="test_user",
            limit=20,
        )

        # 调用被测试的方法
        result = await self.app.conversation.get_messages(self.api_key, query_params)

        # 验证结果
        self.assertIsInstance(result, MessageList)
        self.assertEqual(len(result.data), 2)
        self.assertEqual(result.data[0].id, "msg_123")
        self.assertEqual(result.data[1].id, "msg_456")
        self.assertEqual(result.has_more, False)
        self.assertEqual(result.limit, 20)

        # 验证API调用
        self.api_client.get.assert_called_once_with(
            "/messages",
            params={"conversation_id": "conv_123", "user": "test_user", "limit": 20},
        )

    @pytest.mark.asyncio
    async def test_fetch_messages_with_first_id(self):
        """测试使用first_id参数获取消息列表"""
        # 准备测试数据
        mock_response = {
            "data": [
                {
                    "id": "msg_789",
                    "conversation_id": "conv_123",
                    "inputs": {},
                    "query": "第三个测试问题",
                    "answer": "第三个测试回答",
                    "created_at": 1234567892,
                    "feedback": {},
                    "message_files": [],
                    "agent_thoughts": [],
                    "retriever_resources": [],
                }
            ],
            "has_more": False,
            "limit": 10,
        }

        # 设置模拟返回值
        self.api_client.get.return_value = mock_response

        # 创建查询参数
        query_params = MessageListQueryPayloads(
            conversation_id="conv_123",
            user="test_user",
            first_id="msg_456",
            limit=10,
        )

        # 调用被测试的方法
        result = await self.app.conversation.get_messages(self.api_key, query_params)

        # 验证结果
        self.assertIsInstance(result, MessageList)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0].id, "msg_789")
        self.assertEqual(result.has_more, False)
        self.assertEqual(result.limit, 10)

        # 验证API调用
        self.api_client.get.assert_called_once_with(
            "/messages",
            params={
                "conversation_id": "conv_123",
                "user": "test_user",
                "first_id": "msg_456",
                "limit": 10,
            },
        )

    @pytest.mark.asyncio
    async def test_fetch_messages_with_empty_api_key(self):
        """测试使用空API密钥获取消息列表"""
        # 创建查询参数
        query_params = MessageListQueryPayloads(
            conversation_id="conv_123",
            user="test_user",
        )

        # 调用被测试的方法，预期会抛出ValueError异常
        with self.assertRaises(ValueError) as context:
            await self.app.conversation.get_messages(None, query_params)

        # 验证异常消息
        self.assertEqual(str(context.exception), "API密钥不能为空")

        # 验证API未被调用
        self.api_client.get.assert_not_called()


if __name__ == "__main__":
    unittest.main() 