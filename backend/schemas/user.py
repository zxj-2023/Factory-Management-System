from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .common import TimestampMixin


class UserSyncOut(TimestampMixin):
    id: UUID = Field(..., description="业务用户ID")
    auth_user_id: UUID = Field(..., description="Supabase Auth 用户ID，对应 JWT sub")
    email: str = Field(..., description="邮箱")
    display_name: Optional[str] = Field(None, description="显示名")
    role: str = Field(..., description="业务角色")
    warehouse_id: Optional[str] = Field(None, description="归属仓库（可选）")

    class Config:
        from_attributes = True


class UserOut(UserSyncOut):
    """列表输出与更新返回可复用。"""


class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, description="显示名")
    role: str = Field(..., description="业务角色")
    warehouse_id: Optional[str] = Field(None, description="归属仓库（可选）")

    class Config:
        extra = "forbid"
