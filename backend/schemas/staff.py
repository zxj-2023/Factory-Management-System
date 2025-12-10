"""
员工（staff）相关的请求/响应模型。
"""

from typing import Optional

from pydantic import BaseModel, Field

from .common import TimestampMixin


class StaffBase(BaseModel):
    name: str = Field(..., max_length=50, description="员工姓名")
    gender: Optional[str] = Field(None, pattern="^(M|F)$", description="性别，仅 M/F")
    hire_date: str = Field(..., description="入职日期，格式 YYYY-MM-DD")
    title: Optional[str] = Field(None, max_length=50, description="职称/岗位")
    warehouse_id: str = Field(..., max_length=20, description="所属仓库")

    class Config:
        extra = "forbid"


class StaffCreate(StaffBase):
    staff_id: str = Field(..., max_length=20, description="员工编号")


class StaffUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50, description="员工姓名")
    gender: Optional[str] = Field(None, pattern="^(M|F)$", description="性别，仅 M/F")
    hire_date: Optional[str] = Field(None, description="入职日期，格式 YYYY-MM-DD")
    title: Optional[str] = Field(None, max_length=50, description="职称/岗位")
    warehouse_id: Optional[str] = Field(None, max_length=20, description="所属仓库")

    class Config:
        extra = "forbid"


class StaffOut(StaffBase, TimestampMixin):
    staff_id: str = Field(..., max_length=20, description="员工编号")

    class Config:
        orm_mode = True
