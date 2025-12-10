"""
员工（staff）服务层：封装员工的增删改查，供路由调用。
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from schemas.staff import StaffCreate, StaffUpdate
from src.db import models


def list_staff(db: Session, warehouse_id: Optional[str] = None) -> List[models.Staff]:
    query = db.query(models.Staff)
    if warehouse_id:
        query = query.filter(models.Staff.warehouse_id == warehouse_id)
    return query.all()


def get_staff(db: Session, staff_id: str) -> Optional[models.Staff]:
    return db.query(models.Staff).filter(models.Staff.staff_id == staff_id).first()


def create_staff(db: Session, payload: StaffCreate) -> models.Staff:
    staff = models.Staff(**payload.dict())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


def update_staff(db: Session, staff_id: str, payload: StaffUpdate) -> Optional[models.Staff]:
    staff = get_staff(db, staff_id)
    if not staff:
        return None
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(staff, key, value)
    db.commit()
    db.refresh(staff)
    return staff


def delete_staff(db: Session, staff_id: str) -> bool:
    staff = get_staff(db, staff_id)
    if not staff:
        return False
    db.delete(staff)
    db.commit()
    return True
