"""
供应商（supplier）服务层：封装供应商的增删改查，供路由调用。
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from schemas.supplier import SupplierCreate, SupplierUpdate
from src.db import models


def list_suppliers(db: Session, name: Optional[str] = None) -> List[models.Supplier]:
    query = db.query(models.Supplier)
    if name:
        query = query.filter(models.Supplier.name.ilike(f"%{name}%"))
    return query.all()


def get_supplier(db: Session, supplier_id: str) -> Optional[models.Supplier]:
    return db.query(models.Supplier).filter(models.Supplier.supplier_id == supplier_id).first()


def create_supplier(db: Session, payload: SupplierCreate) -> models.Supplier:
    supplier = models.Supplier(**payload.dict())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


def update_supplier(db: Session, supplier_id: str, payload: SupplierUpdate) -> Optional[models.Supplier]:
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        return None
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return supplier


def delete_supplier(db: Session, supplier_id: str) -> bool:
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        return False
    db.delete(supplier)
    db.commit()
    return True
