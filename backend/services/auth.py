"""
认证相关服务：基于 Supabase Auth 的 sub/email，同步/查询业务用户表。
"""

from typing import Optional

from sqlalchemy.orm import Session

from src.db import models

DEFAULT_ROLE = "inventory_operator"


def get_or_create_app_user(
    db: Session,
    auth_user_id: str,
    email: str,
    display_name: Optional[str] = None,
    default_role: str = DEFAULT_ROLE,
) -> models.AppUser:
    user = (
        db.query(models.AppUser)
        .filter(models.AppUser.auth_user_id == auth_user_id)
        .first()
    )
    if user:
        return user

    user = models.AppUser(
        auth_user_id=auth_user_id,
        email=email,
        display_name=display_name,
        role=default_role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
