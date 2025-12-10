"""
通用 Schema 片段定义。

TimestampMixin 提供 created_at / updated_at 字段，供各资源的输出模型复用，
保持时间戳信息透传而不重复定义。
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = Field(default=None, description="创建时间（数据库默认 now()）")
    updated_at: Optional[datetime] = Field(default=None, description="更新时间（触发器自动更新）")

    class Config:
        extra = "forbid"
        from_attributes = True
