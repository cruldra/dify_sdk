# Dify SDK - 知识库模块示例

本目录包含使用Dify SDK的知识库模块的示例代码。

## 示例列表

1. [创建知识库](./create.py) - 展示如何创建Dify知识库
2. [查询知识库列表](./find_list.py) - 展示如何查询Dify知识库列表
3. [删除知识库](./delete.py) - 展示如何删除Dify知识库

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

# 查询知识库列表示例
python examples/dataset/find_list.py

# 删除知识库示例
python examples/dataset/delete.py
```

## 知识库模块功能

知识库模块提供了以下功能：

- `create(payload)` - 创建新的知识库
  - `payload`: 知识库创建参数，类型为`DataSetCreatePayloads`

- `find_list(page, limit, include_all, tag_ids)` - 查询知识库列表
  - `page`: 页码，默认为1
  - `limit`: 每页数量，默认为30
  - `include_all`: 是否包含所有知识库，默认为False
  - `tag_ids`: 标签ID列表，用于筛选特定标签的知识库，默认为None

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

### 查询知识库列表

```python
# 初始化AdminClient和DifyDataset
admin_client = AdminClient(BASE_URL, API_KEY)
dify_dataset = DifyDataset(admin_client)

# 查询所有知识库
dataset_list = await dify_dataset.find_list()
print(f"总知识库数: {dataset_list.total}")
print(f"当前页知识库数: {len(dataset_list.data)}")

# 分页查询知识库
page = 1
limit = 10
dataset_list = await dify_dataset.find_list(page=page, limit=limit)
print(f"第{page}页（每页{limit}条）知识库数: {len(dataset_list.data)}")

# 根据标签查询知识库
tag_ids = ["your_tag_id"]
dataset_list = await dify_dataset.find_list(tag_ids=tag_ids)
print(f"标签筛选后的知识库数: {len(dataset_list.data)}")

# 查询所有知识库（包括共享的）
dataset_list = await dify_dataset.find_list(include_all=True)
print(f"所有知识库数: {dataset_list.total}")
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