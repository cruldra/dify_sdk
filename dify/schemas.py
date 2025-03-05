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


class Error(BaseModel):
    """错误模型

    Attributes:
        code: 错误码
        message: 错误信息
    """

    code: str = Field(description="错误码")
    message: str = Field(description="错误信息")

class Pair(BaseModel, Generic[T]):
    """泛型对类型，包含一个值和一个错误

    Attributes:
        value: 值
        error: 错误信息
    """

    value: Optional[T] = Field(default=None, description="值")
    error: Optional[Error] = Field(default=None, description="错误信息")

    def is_ok(self) -> bool:
        """判断是否成功"""
        return self.error is None

    def is_err(self) -> bool:
        """判断是否失败"""
        return self.error is not None

    def unwrap(self) -> T:
        """获取值，如果存在错误则抛出异常"""
        if self.is_err():
            raise ValueError(f"Unwrap failed: {self.error}")
        return self.value

    def unwrap_or(self, default: T) -> T:
        """获取值，如果存在错误则返回默认值"""
        return self.value if self.is_ok() else default
