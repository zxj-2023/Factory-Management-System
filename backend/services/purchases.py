"""
采购（purchase）服务层：封装采购单的增删改查，供路由调用。
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from schemas.purchase import PurchaseCreate, PurchaseUpdate
from src.db import models


def list_purchases(
    db: Session,
    warehouse_id: Optional[str] = None,
    supplier_id: Optional[str] = None,
    part_id: Optional[str] = None,
) -> List[models.Purchase]:
    query = db.query(models.Purchase)
    if warehouse_id:
        query = query.filter(models.Purchase.warehouse_id == warehouse_id)
    if supplier_id:
        query = query.filter(models.Purchase.supplier_id == supplier_id)
    if part_id:
        query = query.filter(models.Purchase.part_id == part_id)
    return query.all()


def get_purchase(db: Session, purchase_id: str) -> Optional[models.Purchase]:
    return db.query(models.Purchase).filter(models.Purchase.purchase_id == purchase_id).first()


def create_purchase(db: Session, payload: PurchaseCreate) -> models.Purchase:
    record = models.Purchase(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_purchase(db: Session, purchase_id: str, payload: PurchaseUpdate) -> Optional[models.Purchase]:
    record = get_purchase(db, purchase_id)
    if not record:
        return None
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


def delete_purchase(db: Session, purchase_id: str) -> bool:
    record = get_purchase(db, purchase_id)
    if not record:
        return False
    db.delete(record)
    db.commit()
    return True
