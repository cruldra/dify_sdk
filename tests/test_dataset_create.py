"""
测试知识库创建功能
"""

from unittest.mock import AsyncMock

import pytest

from dify.dataset import DifyDataset
from dify.dataset.schemas import (
    DataSetCreatePayloads,
    DataSource,
    InfoList,
    FileInfoList,
    DataSetCreateResponse
)


@pytest.mark.asyncio
async def test_create():
    """测试create方法"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()

    # 设置模拟响应数据
    mock_response = {
        "dataset": {
            "id": "test_dataset_id",
            "name": "test_dataset",
            "description": None,
            "permission": "only_me",
            "data_source_type": "upload_file",
            "indexing_technique": "high_quality",
            "created_by": "test_user",
            "created_at": 1630000000
        },
        "documents": [
            {
                "id": "test_doc_id",
                "position": 0,
                "data_source_type": "upload_file",
                "data_source_info": {"file_id": "test_file_id"},
                "data_source_detail_dict": {"file_name": "test.txt"},
                "dataset_process_rule_id": "test_rule_id",
                "name": "test.txt",
                "created_from": "web",
                "created_by": "test_user",
                "created_at": 1630000000,
                "tokens": 100,
                "indexing_status": "waiting",
                "error": None,
                "enabled": True,
                "disabled_at": None,
                "disabled_by": None,
                "archived": False,
                "display_status": "queuing",
                "word_count": 50,
                "hit_count": 0,
                "doc_form": "text_model"
            }
        ]
    }

    # 设置模拟方法的返回值
    mock_admin_client.post.return_value = mock_response

    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)

    # 创建测试参数
    create_payload = DataSetCreatePayloads(
        data_source=DataSource(
            type="upload_file",
            info_list=InfoList(
                data_source_type="upload_file",
                file_info_list=FileInfoList(
                    file_ids=["test_file_id"]
                )
            )
        ),
        indexing_technique="high_quality",
        doc_form="text_model",
        doc_language="Chinese",
        embedding_model="text-embedding-3-large",
        embedding_model_provider="langgenius/openai/openai"
    )

    # 调用create方法
    result = await dify_dataset.create(create_payload)

    # 验证结果
    assert isinstance(result, DataSetCreateResponse)
    assert result.dataset.id == "test_dataset_id"
    assert result.dataset.name == "test_dataset"
    assert result.dataset.indexing_technique == "high_quality"
    assert len(result.documents) == 1
    assert result.documents[0].id == "test_doc_id"
    assert result.documents[0].name == "test.txt"

    # 验证调用了正确的API路径和参数
    mock_admin_client.post.assert_called_once()
    call_args = mock_admin_client.post.call_args
    assert call_args[0][0] == "/datasets/init"

    # 验证传递的JSON数据
    json_data = call_args[1]["json"]
    assert json_data["data_source"]["type"] == "upload_file"
    assert json_data["indexing_technique"] == "high_quality"
    assert json_data["doc_form"] == "text_model"
    assert json_data["doc_language"] == "Chinese"
    assert json_data["embedding_model"] == "text-embedding-3-large"
    assert json_data["embedding_model_provider"] == "langgenius/openai/openai"


@pytest.mark.asyncio
async def test_create_empty_payload():
    """测试create方法，当参数为空时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()

    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)

    # 调用create方法，应该抛出ValueError
    with pytest.raises(ValueError, match="知识库创建参数不能为空"):
        await dify_dataset.create(None)


@pytest.mark.asyncio
async def test_create_http_error():
    """测试create方法，当HTTP请求失败时"""
    # 创建模拟的AdminClient
    mock_admin_client = AsyncMock()

    # 设置模拟方法抛出异常
    import httpx
    mock_admin_client.post.side_effect = httpx.HTTPStatusError(
        "400 Bad Request",
        request=httpx.Request("POST", "http://example.com"),
        response=httpx.Response(400)
    )

    # 创建DifyDataset实例
    dify_dataset = DifyDataset(mock_admin_client)

    # 创建测试参数
    create_payload = DataSetCreatePayloads(
        data_source=DataSource(
            type="upload_file",
            info_list=InfoList(
                data_source_type="upload_file",
                file_info_list=FileInfoList(
                    file_ids=["test_file_id"]
                )
            )
        ),
        indexing_technique="high_quality"
    )

    # 调用create方法，应该抛出HTTPStatusError
    with pytest.raises(httpx.HTTPStatusError):
        await dify_dataset.create(create_payload)
