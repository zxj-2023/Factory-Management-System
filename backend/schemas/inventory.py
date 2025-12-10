"""
库存（inventory）相关的请求/响应模型。
包含创建、更新、调整库存的结构定义，复合主键由 warehouse_id + part_id 组成。
"""

from typing import Optional

from pydantic import BaseModel, Field

from .common import TimestampMixin


class InventoryBase(BaseModel):
    warehouse_id: str = Field(..., max_length=20, description="仓库编号")
    part_id: str = Field(..., max_length=20, description="零件编号")
    stock_quantity: int = Field(..., ge=0, description="库存数量，非负")

    class Config:
        extra = "forbid"


class InventoryCreate(InventoryBase):
    """创建库存记录（复合主键需唯一）。"""


class InventoryUpdate(BaseModel):
    stock_quantity: int = Field(..., ge=0, description="库存数量，非负")

    class Config:
        extra = "forbid"


class InventoryAdjust(BaseModel):
    delta: int = Field(..., description="库存增减量，正数增加，负数减少；结果不得为负")

    class Config:
        extra = "forbid"


class InventoryOut(InventoryBase, TimestampMixin):
    class Config:
        orm_mode = True
