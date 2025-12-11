from typing import Optional

from pydantic import BaseModel, Field

from .common import TimestampMixin


class UserSyncOut(TimestampMixin):
    id: str = Field(..., description="业务用户ID")
    auth_user_id: str = Field(..., description="Supabase Auth 用户ID，对应 JWT sub")
    email: str = Field(..., description="邮箱")
    display_name: Optional[str] = Field(None, description="显示名")
    role: str = Field(..., description="业务角色")
    warehouse_id: Optional[str] = Field(None, description="归属仓库（可选）")

    class Config:
        from_attributes = True
