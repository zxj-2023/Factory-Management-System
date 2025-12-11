"""
用户权限管理服务：列表与更新 app_user。
仅 admin 权限应调用。
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from schemas.user import UserUpdate
from src.db import models

ALLOWED_ROLES = {"admin", "warehouse_manager", "purchaser", "inventory_operator"}


def list_users(db: Session, email: Optional[str] = None, role: Optional[str] = None, warehouse_id: Optional[str] = None) -> List[models.AppUser]:
    query = db.query(models.AppUser)
    if email:
        query = query.filter(models.AppUser.email.ilike(f"%{email}%"))
    if role:
        query = query.filter(models.AppUser.role == role)
    if warehouse_id:
        query = query.filter(models.AppUser.warehouse_id == warehouse_id)
    return query.order_by(models.AppUser.created_at.desc()).all()


def update_user(db: Session, user_id: str, payload: UserUpdate) -> Optional[models.AppUser]:
    user = db.query(models.AppUser).filter(models.AppUser.id == user_id).first()
    if not user:
        return None
    if payload.role and payload.role not in ALLOWED_ROLES:
        raise ValueError("Invalid role")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
