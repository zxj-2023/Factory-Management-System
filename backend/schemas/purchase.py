"""
采购（purchase）相关的请求/响应模型。
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from .common import TimestampMixin


class PurchaseBase(BaseModel):
    part_id: str = Field(..., max_length=20, description="零件编号")
    supplier_id: str = Field(..., max_length=20, description="供应商编号")
    warehouse_id: str = Field(..., max_length=20, description="入库仓库编号")
    purchase_date: date = Field(..., description="采购日期")
    quantity: int = Field(..., gt=0, description="采购数量，正数")
    actual_price: float = Field(..., gt=0, description="实际采购单价，正数")

    class Config:
        extra = "forbid"


class PurchaseCreate(PurchaseBase):
    purchase_id: str = Field(..., max_length=30, description="采购单号")


class PurchaseUpdate(BaseModel):
    part_id: Optional[str] = Field(None, max_length=20, description="零件编号")
    supplier_id: Optional[str] = Field(None, max_length=20, description="供应商编号")
    warehouse_id: Optional[str] = Field(None, max_length=20, description="入库仓库编号")
    purchase_date: Optional[date] = Field(None, description="采购日期")
    quantity: Optional[int] = Field(None, gt=0, description="采购数量，正数")
    actual_price: Optional[float] = Field(None, gt=0, description="实际采购单价，正数")

    class Config:
        extra = "forbid"


class PurchaseOut(PurchaseBase, TimestampMixin):
    purchase_id: str = Field(..., max_length=30, description="采购单号")

    class Config:
        orm_mode = True
