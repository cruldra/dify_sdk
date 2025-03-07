from typing import List, Optional
from pydantic import BaseModel, Field

from dify.tag import Tag


class KeywordSetting(BaseModel):
    """关键词权重设置Schema

    Attributes:
        keyword_weight: 关键词权重，取值范围0-1，默认0.3
    """

    keyword_weight: float = Field(default=0.3, ge=0, le=1, description="关键词权重")

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class VectorSetting(BaseModel):
    """向量权重设置Schema

    Attributes:
        vector_weight: 向量权重，取值范围0-1，默认0.7
        embedding_provider_name: 嵌入模型提供商名称
        embedding_model_name: 嵌入模型名称
    """

    vector_weight: float = Field(default=0.7, ge=0, le=1, description="向量权重")
    embedding_provider_name: str = Field(default="", description="嵌入模型提供商名称")
    embedding_model_name: str = Field(default="", description="嵌入模型名称")

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class Weights(BaseModel):
    """权重设置Schema

    Attributes:
        keyword_setting: 关键词权重设置
        vector_setting: 向量权重设置
    """

    weight_type: str = Field(default="customized", description="权重类型")
    vector_setting: VectorSetting = Field(
        default=VectorSetting(), description="向量权重设置"
    )
    keyword_setting: KeywordSetting = Field(
        default=KeywordSetting(), description="关键词权重设置"
    )

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class RerankingModel(BaseModel):
    """重排序设置Schema

    Attributes:
        reranking_provider_name: 重排序模型提供商名称
        reranking_model_name: 重排序模型名称
    """

    reranking_provider_name: str = Field(
        default="langgenius/tongyi/tongyi", description="重排序模型提供商名称"
    )
    reranking_model_name: str = Field(
        default="gte-rerank", description="重排序模型名称"
    )

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class RetrievalModel(BaseModel):
    """检索模型Schema

    Attributes:
        search_method: 搜索方法
        reranking_enable: 是否启用重排序
        reranking_model: 重排序模型设置
        top_k: 返回结果数量
        score_threshold_enabled: 是否启用分数阈值
        score_threshold: 分数阈值
        reranking_mode: 重排序模式
        weights: 权重设置
    """

    search_method: str = Field(default="hybrid_search", description="搜索方法")
    reranking_enable: bool = Field(default=True, description="是否启用重排序")
    reranking_model: RerankingModel = Field(
        default=RerankingModel(), description="重排序模型设置"
    )
    top_k: int = Field(default=3, description="返回结果数量")
    score_threshold_enabled: bool = Field(default=False, description="是否启用分数阈值")
    score_threshold: float = Field(default=0.5, description="分数阈值")
    reranking_mode: str = Field(default="reranking_model", description="重排序模式")
    weights: Weights = Field(default=Weights(), description="权重设置")

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class ProcessRule(BaseModel):
    """数据处理规则Schema

    Attributes:
        rules: 预处理规则配置
        mode: 处理模式
    """

    rules: dict = Field(
        default={
            "pre_processing_rules": [
                {"id": "remove_extra_spaces", "enabled": True},
                {"id": "remove_urls_emails", "enabled": False},
            ],
            "segmentation": {
                "separator": "\n\n",
                "max_tokens": 500,
                "chunk_overlap": 50,
            },
        },
        description="预处理规则配置",
    )
    mode: str = Field(default="custom", description="处理模式")

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class FileInfoList(BaseModel):
    """文件信息列表Schema

    Attributes:
        file_ids: 文件ID列表
    """

    file_ids: List[str] = Field(default_factory=list, description="文件ID列表")


class InfoList(BaseModel):
    data_source_type: str = Field(default="upload_file", description="数据源类型")
    file_info_list: FileInfoList = Field(
        default=FileInfoList(), description="文件信息列表"
    )


class DataSource(BaseModel):
    """数据源Schema

    Attributes:
        data_source_type: 数据源类型
        file_info_list: 文件信息列表
    """

    type: str = Field(default="upload_file", description="数据源类型")
    info_list: InfoList = Field(default=InfoList(), description="文件信息列表")


class DataSetCreatePayloads(BaseModel):
    """数据集创建请求Schema

    Attributes:
        data_source: 数据源配置
        indexing_technique: 索引技术
        process_rule: 处理规则
        doc_form: 文档格式
        doc_language: 文档语言
        retrieval_model: 检索模型配置
        embedding_model: 嵌入模型
        embedding_model_provider: 嵌入模型提供商
    """

    data_source: DataSource = Field(description="数据源配置")
    indexing_technique: str = Field(default="high_quality", description="索引技术")
    process_rule: ProcessRule = Field(default=ProcessRule(), description="处理规则")
    doc_form: str = Field(default="text_model", description="文档格式")
    doc_language: str = Field(default="Chinese", description="文档语言")
    retrieval_model: RetrievalModel = Field(
        default=RetrievalModel(), description="检索模型配置"
    )
    embedding_model: str = Field(
        default="text-embedding-3-large", description="嵌入模型"
    )
    embedding_model_provider: str = Field(
        default="langgenius/openai/openai", description="嵌入模型提供商"
    )

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class DataSetInCreate(BaseModel):
    """数据集Schema

    Attributes:
        id: 数据集ID
        name: 数据集名称
        description: 数据集描述
        permission: 数据集权限
        data_source_type: 数据源类型
        indexing_technique: 索引技术
        created_by: 创建者ID
        created_at: 创建时间戳
    """

    id: str = Field(description="数据集ID")
    name: str = Field(description="数据集名称")
    description: Optional[str] = Field(default=None, description="数据集描述")
    permission: Optional[str] = Field(default="only_me", description="数据集权限")
    data_source_type: Optional[str] = Field(
        default="upload_file", description="数据源类型"
    )
    indexing_technique: Optional[str] = Field(
        default="high_quality", description="索引技术"
    )
    created_by: Optional[str] = Field(description="创建者ID")
    created_at: Optional[int] = Field(description="创建时间戳")

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class Document(BaseModel):
    """文档Schema

    Attributes:
        id: 文档ID
        data_source_type: 数据源类型
        data_source_info: 数据源信息
        data_source_detail_dict: 数据源详细信息
        dataset_process_rule_id: 数据集处理规则ID
        name: 文档名称
        created_from: 创建来源
        created_by: 创建者ID
        created_at: 创建时间戳
        tokens: 文档token数
        indexing_status: 索引状态
        error: 错误信息
        enabled: 是否启用
        disabled_at: 禁用时间
        disabled_by: 禁用者
        archived: 是否归档
        display_status: 显示状态
        word_count: 字数统计
        hit_count: 命中次数
        doc_form: 文档格式
    """

    id: str = Field(description="文档ID")
    position: int = Field(description="文档位置")
    data_source_type: str = Field(default="upload_file", description="数据源类型")
    data_source_info: dict = Field(description="数据源信息")
    data_source_detail_dict: dict = Field(description="数据源详细信息")
    dataset_process_rule_id: str = Field(description="数据集处理规则ID")
    name: str = Field(description="文档名称")
    created_from: str = Field(description="创建来源")
    created_by: str = Field(description="创建者ID")
    created_at: int = Field(description="创建时间戳")
    tokens: int = Field(default=0, description="文档token数")
    indexing_status: str = Field(default="waiting", description="索引状态")
    error: Optional[str] = Field(default=None, description="错误信息")
    enabled: bool = Field(default=True, description="是否启用")
    disabled_at: Optional[int] = Field(default=None, description="禁用时间")
    disabled_by: Optional[str] = Field(default=None, description="禁用者")
    archived: bool = Field(default=False, description="是否归档")
    display_status: str = Field(default="queuing", description="显示状态")
    word_count: int = Field(default=0, description="字数统计")
    hit_count: int = Field(default=0, description="命中次数")
    doc_form: str = Field(default="text_model", description="文档格式")

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class DataSetCreateResponse(BaseModel):
    """数据集创建响应Schema

    Attributes:
        dataset: 数据集
        documents: 文档列表
    """

    dataset: DataSetInCreate = Field(description="数据集")
    documents: List[Document] = Field(description="文档列表")
    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class DataSetInList(BaseModel):
    """数据集列表Schema

    Attributes:
        id: 数据集ID
        name: 数据集名称
        description: 数据集描述
        tags: 数据集标签
    """

    id: str = Field(description="数据集ID")
    name: str = Field(description="数据集名称")
    description: Optional[str] = Field(default=None, description="数据集描述")
    tags: Optional[List[Tag]] = Field(default=None, description="数据集标签")
    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


class DataSetList(BaseModel):
    """知识库列表Schema

    Attributes:
        data: 知识库列表
        total: 知识库总数
        has_more: 是否有更多知识库
    """

    data: List[DataSetInList] = Field(default_factory=list, description="知识库列表")
    total: int = Field(default=0, description="知识库总数")
    has_more: bool = Field(default=False, description="是否有更多知识库")

    # Pydantic V2 配置
    model_config = {
        "populate_by_name": True,
        "protected_namespaces": (),
    }


__all__ = [
    "KeywordSetting",
    "VectorSetting",
    "Weights",
    "RerankingModel",
    "RetrievalModel",
    "ProcessRule",
    "FileInfoList",
    "InfoList",
    "DataSource",
    "DataSetCreatePayloads",
    "DataSetCreateResponse",
    "DataSetInList",
    "Document",
    "DataSetInCreate",
    "DataSetList",
]
