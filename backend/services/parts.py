"""
零件（part）服务层：封装对零件的增删改查，供路由调用。
使用 SQLAlchemy Session 直接操作 ORM 模型。
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from schemas.part import PartCreate, PartOut, PartUpdate
from src.db import models


def list_parts(db: Session, part_type: Optional[str] = None) -> List[models.Part]:
    query = db.query(models.Part)
    if part_type:
        query = query.filter(models.Part.type == part_type)
    return query.all()


def get_part(db: Session, part_id: str) -> Optional[models.Part]:
    return db.query(models.Part).filter(models.Part.part_id == part_id).first()


def create_part(db: Session, payload: PartCreate) -> models.Part:
    part = models.Part(**payload.dict())
    db.add(part)
    db.commit()
    db.refresh(part)
    return part


def update_part(db: Session, part_id: str, payload: PartUpdate) -> Optional[models.Part]:
    part = get_part(db, part_id)
    if not part:
        return None
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(part, key, value)
    db.commit()
    db.refresh(part)
    return part


def delete_part(db: Session, part_id: str) -> bool:
    part = get_part(db, part_id)
    if not part:
        return False
    db.delete(part)
    db.commit()
    return True
