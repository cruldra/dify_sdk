#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试对话列表功能
"""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from dify.app import DifyApp
from dify.app.schemas import ApiKey, ConversationList, ConversationListQueryPayloads, SortBy, OperationResult


class TestConversations(unittest.TestCase):
    """测试对话列表相关功能"""

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
    async def test_fetch_conversations_with_valid_params(self):
        """测试使用有效参数获取对话列表"""
        # 准备测试数据
        mock_response = {
            "data": [
                {
                    "id": "conv_123",
                    "name": "测试对话1",
                    "inputs": {},
                    "status": "normal",
                    "introduction": "这是一个测试对话",
                    "created_at": 1234567890,
                    "updated_at": 1234567890,
                },
                {
                    "id": "conv_456",
                    "name": "测试对话2",
                    "inputs": {},
                    "status": "normal",
                    "introduction": "这是另一个测试对话",
                    "created_at": 1234567891,
                    "updated_at": 1234567891,
                },
            ],
            "has_more": False,
            "limit": 2,
        }
        self.api_client.get.return_value = mock_response

        # 创建查询参数
        query_params = ConversationListQueryPayloads(
            user="test_user",
            limit=2,
            sort_by=SortBy.UPDATED_AT_DESC,
        )

        # 调用测试方法
        result = await self.app.fetch_conversations(self.api_key, query_params)

        # 验证结果
        self.assertIsInstance(result, ConversationList)
        self.assertEqual(len(result.data), 2)
        self.assertEqual(result.data[0].id, "conv_123")
        self.assertEqual(result.data[1].id, "conv_456")
        self.assertFalse(result.has_more)
        self.assertEqual(result.limit, 2)

        # 验证API调用
        self.api_client.get.assert_called_once_with(
            "/conversations",
            params={"user": "test_user", "limit": 2, "sort_by": "updated_at"},
        )

    @pytest.mark.asyncio
    async def test_fetch_conversations_with_last_id(self):
        """测试使用last_id参数获取对话列表"""
        # 准备测试数据
        mock_response = {
            "data": [
                {
                    "id": "conv_789",
                    "name": "测试对话3",
                    "inputs": {},
                    "status": "normal",
                    "introduction": "这是第三个测试对话",
                    "created_at": 1234567892,
                    "updated_at": 1234567892,
                },
            ],
            "has_more": False,
            "limit": 1,
        }
        self.api_client.get.return_value = mock_response

        # 创建查询参数
        query_params = ConversationListQueryPayloads(
            user="test_user",
            last_id="conv_456",
            limit=1,
            sort_by=SortBy.CREATED_AT_ASC,
        )

        # 调用测试方法
        result = await self.app.fetch_conversations(self.api_key, query_params)

        # 验证结果
        self.assertIsInstance(result, ConversationList)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0].id, "conv_789")
        self.assertFalse(result.has_more)
        self.assertEqual(result.limit, 1)

        # 验证API调用
        self.api_client.get.assert_called_once_with(
            "/conversations",
            params={
                "user": "test_user",
                "last_id": "conv_456",
                "limit": 1,
                "sort_by": "created_at",
            },
        )

    @pytest.mark.asyncio
    async def test_fetch_conversations_with_empty_api_key(self):
        """测试使用空API密钥获取对话列表"""
        # 创建查询参数
        query_params = ConversationListQueryPayloads(
            user="test_user",
            limit=10,
        )

        # 调用测试方法并验证异常
        with self.assertRaises(ValueError) as context:
            await self.app.fetch_conversations(None, query_params)

        self.assertEqual(str(context.exception), "API密钥不能为空")

    @pytest.mark.asyncio
    async def test_stop_message_with_valid_params(self):
        """测试使用有效参数停止消息生成"""
        # 准备测试数据
        mock_response = {"result": "success"}
        self.api_client.post.return_value = mock_response

        # 调用测试方法
        result = await self.app.stop_message(self.api_key, "task_123", "user_123")

        # 验证结果
        self.assertIsInstance(result, OperationResult)
        self.assertEqual(result.result, "success")

        # 验证API调用
        self.api_client.post.assert_called_once_with(
            "/chat-messages/task_123/stop",
            json={"user": "user_123"},
        )

    @pytest.mark.asyncio
    async def test_stop_message_with_empty_api_key(self):
        """测试使用空API密钥停止消息生成"""
        # 调用测试方法并验证异常
        with self.assertRaises(ValueError) as context:
            await self.app.stop_message(None, "task_123", "user_123")

        self.assertEqual(str(context.exception), "API密钥不能为空")

    @pytest.mark.asyncio
    async def test_stop_message_with_empty_task_id(self):
        """测试使用空任务ID停止消息生成"""
        # 调用测试方法并验证异常
        with self.assertRaises(ValueError) as context:
            await self.app.stop_message(self.api_key, "", "user_123")

        self.assertEqual(str(context.exception), "任务ID不能为空")

    @pytest.mark.asyncio
    async def test_stop_message_with_empty_user_id(self):
        """测试使用空用户ID停止消息生成"""
        # 调用测试方法并验证异常
        with self.assertRaises(ValueError) as context:
            await self.app.stop_message(self.api_key, "task_123", "")

        self.assertEqual(str(context.exception), "用户ID不能为空")


if __name__ == "__main__":
    unittest.main() 