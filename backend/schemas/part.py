"""
零件（part）相关的请求/响应模型。
区分创建、更新、输出，确保路由输入校验与数据库约束一致。
"""

from typing import Optional

from pydantic import BaseModel, Field

from .common import TimestampMixin


class PartBase(BaseModel):
    name: str = Field(..., max_length=100, description="零件名称")
    unit_price: float = Field(..., ge=0, description="单价，非负")
    type: str = Field(..., max_length=50, description="零件类型/分类")

    class Config:
        extra = "forbid"


class PartCreate(PartBase):
    part_id: str = Field(..., max_length=20, description="零件编号")


class PartUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="零件名称")
    unit_price: Optional[float] = Field(None, ge=0, description="单价，非负")
    type: Optional[str] = Field(None, max_length=50, description="零件类型/分类")

    class Config:
        extra = "forbid"


class PartOut(PartBase, TimestampMixin):
    part_id: str = Field(..., max_length=20, description="零件编号")

    class Config:
        from_attributes = True
