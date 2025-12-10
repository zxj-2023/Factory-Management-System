"""
供应商（supplier）相关的请求/响应模型。
"""

from typing import Optional

from pydantic import BaseModel, Field

from .common import TimestampMixin


class SupplierBase(BaseModel):
    name: str = Field(..., max_length=100, description="供应商名称")
    address: Optional[str] = Field(None, max_length=200, description="地址")
    phone: Optional[str] = Field(None, max_length=20, description="电话")

    class Config:
        extra = "forbid"


class SupplierCreate(SupplierBase):
    supplier_id: str = Field(..., max_length=20, description="供应商编号")


class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="供应商名称")
    address: Optional[str] = Field(None, max_length=200, description="地址")
    phone: Optional[str] = Field(None, max_length=20, description="电话")

    class Config:
        extra = "forbid"


class SupplierOut(SupplierBase, TimestampMixin):
    supplier_id: str = Field(..., max_length=20, description="供应商编号")

    class Config:
        orm_mode = True
