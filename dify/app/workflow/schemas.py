from typing import List, Optional

from pydantic import BaseModel, Field


class Position(BaseModel):
    """位置"""

    x: Optional[float] = Field(default=None, description="x坐标")
    y: Optional[float] = Field(default=None, description="y坐标")


class WorkflowNodeData(BaseModel):
    """工作流节点数据"""

    type: Optional[str] = Field(default=None, description="节点类型")
    title: Optional[str] = Field(default=None, description="节点标题")
    selected: Optional[bool] = Field(default=False, description="是否被选中")
    desc: Optional[str] = Field(default=None, description="节点描述")


class WorkflowNode(BaseModel):
    """工作流节点"""

    data: Optional[WorkflowNodeData] = Field(default=None, description="节点数据")
    height: Optional[int] = Field(default=None, description="节点高度")
    id: Optional[str] = Field(default=None, description="节点ID")
    position: Optional[Position] = Field(default=None, description="节点位置")
    position_absolute: Optional[Position] = Field(
        default=None, description="节点绝对位置"
    )
    selected: Optional[bool] = Field(default=False, description="是否被选中")
    source_position: Optional[str] = Field(default=None, description="源位置")
    target_position: Optional[str] = Field(default=None, description="目标位置")
    type: Optional[str] = Field(default=None, description="节点类型")
    width: Optional[int] = Field(default=None, description="节点宽度")


class WorkflowEdgeData(BaseModel):
    """工作流边数据"""

    isInIteration: Optional[bool] = Field(default=False, description="是否在迭代中")
    sourceType: Optional[str] = Field(default=None, description="起始节点类型")
    targetType: Optional[str] = Field(default=None, description="目标节点类型")


class WorkflowEdge(BaseModel):
    """工作流边"""

    data: Optional[WorkflowEdgeData] = Field(default=None, description="边数据")
    id: Optional[str] = Field(default=None, description="边ID")
    source: Optional[str] = Field(default=None, description="起始节点ID")
    sourceHandle: Optional[str] = Field(default=None, description="起始节点句柄")
    target: Optional[str] = Field(default=None, description="目标节点ID")
    targetHandle: Optional[str] = Field(default=None, description="目标节点句柄")
    type: Optional[str] = Field(default=None, description="边类型")
    zIndex: Optional[int] = Field(default=0, description="z轴索引")


class WorkflowGraph(BaseModel):
    """工作流图"""

    nodes: List[WorkflowNode] = Field(default_factory=list, description="节点列表")
    edges: List[WorkflowEdge] = Field(default_factory=list, description="边列表")


class WorkflowPublish(BaseModel):
    """工作流发布详情"""

    id: str = Field(description="工作流ID")
    graph: WorkflowGraph = Field(description="工作流图")
