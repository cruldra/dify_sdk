# Dify SDK - 知识库模块示例

本目录包含使用Dify SDK的知识库模块的示例代码。

## 示例列表

1. [创建知识库](./create.py) - 展示如何创建Dify知识库
2. [删除知识库](./delete.py) - 展示如何删除Dify知识库

## 使用方法

### 环境准备

在运行示例之前，请确保您已经设置了必要的环境变量：

```bash
# .env文件
DIFY_ADMIN_KEY=your_admin_api_key
DIFY_BASE_URL=your_dify_base_url  # 例如：https://api.dify.ai 或您的自托管URL
```

### 运行示例

使用以下命令运行示例：

```bash
# 创建知识库示例
python examples/dataset/create.py

# 删除知识库示例
python examples/dataset/delete.py
```

## 知识库模块功能

知识库模块提供了以下功能：

- `create(payload)` - 创建新的知识库
  - `payload`: 知识库创建参数，类型为`DataSetCreatePayloads`

- `delete(dataset_id)` - 删除指定ID的知识库
  - `dataset_id`: 要删除的知识库ID

## 使用示例

### 创建知识库

```python
# 初始化AdminClient和DifyDataset
admin_client = AdminClient(BASE_URL, API_KEY)
dify_dataset = DifyDataset(admin_client)

# 创建知识库参数
create_payload = DataSetCreatePayloads(
    data_source=DataSource(
        type="upload_file",
        info_list=InfoList(
            data_source_type="upload_file",
            file_info_list=FileInfoList(
                file_ids=["your_file_id"]
            )
        )
    ),
    indexing_technique="high_quality",
    doc_form="text_model",
    doc_language="Chinese",
    embedding_model="text-embedding-3-large",
    embedding_model_provider="langgenius/openai/openai"
)

# 创建知识库
result = await dify_dataset.create(create_payload)
print(f"知识库ID: {result.dataset.id}")
```

### 删除知识库

```python
# 初始化AdminClient和DifyDataset
admin_client = AdminClient(BASE_URL, API_KEY)
dify_dataset = DifyDataset(admin_client)

# 删除知识库
dataset_id = "your_dataset_id"
try:
    result = await dify_dataset.delete(dataset_id)
    if result:
        print("知识库删除成功")
except Exception as e:
    print(f"删除知识库时出错: {e}")
``` 