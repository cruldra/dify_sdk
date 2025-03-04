from typing import Generic, TypeVar, Optional, List

from pydantic import BaseModel, Field

T = TypeVar("T")


class Pagination(BaseModel, Generic[T]):
    """分页请求模型

    Attributes:
        page: 当前页码
        limit: 每页条数
        total: 总条数
        has_more: 是否有更多数据
        data: 数据列表
    """

    page: int = Field(default=1, description="当前页码")
    limit: int = Field(default=10, description="每页条数")
    total: Optional[int] = Field(default=None, description="总条数")
    has_more: Optional[bool] = Field(default=None, description="是否有更多数据")
    data: Optional[List[T]] = Field(default=None, description="数据列表")
