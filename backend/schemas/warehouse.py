"""
仓库（warehouse）相关的请求/响应模型。
"""

from pydantic import BaseModel, Field

from .common import TimestampMixin


class WarehouseBase(BaseModel):
    address: str = Field(..., max_length=200, description="仓库地址")

    class Config:
        extra = "forbid"


class WarehouseCreate(WarehouseBase):
    warehouse_id: str = Field(..., max_length=20, description="仓库编号")


class WarehouseUpdate(WarehouseBase):
    """全量更新，字段必填。"""


class WarehouseOut(WarehouseBase, TimestampMixin):
    warehouse_id: str = Field(..., max_length=20, description="仓库编号")

    class Config:
        from_attributes = True
