"""
仓库（warehouse）服务层：封装仓库的增删改查，供路由调用。
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from schemas.warehouse import WarehouseCreate, WarehouseUpdate
from src.db import models


def list_warehouses(db: Session) -> List[models.Warehouse]:
    return db.query(models.Warehouse).all()


def get_warehouse(db: Session, warehouse_id: str) -> Optional[models.Warehouse]:
    return db.query(models.Warehouse).filter(models.Warehouse.warehouse_id == warehouse_id).first()


def create_warehouse(db: Session, payload: WarehouseCreate) -> models.Warehouse:
    warehouse = models.Warehouse(**payload.dict())
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


def update_warehouse(db: Session, warehouse_id: str, payload: WarehouseUpdate) -> Optional[models.Warehouse]:
    warehouse = get_warehouse(db, warehouse_id)
    if not warehouse:
        return None
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(warehouse, key, value)
    db.commit()
    db.refresh(warehouse)
    return warehouse


def delete_warehouse(db: Session, warehouse_id: str) -> bool:
    warehouse = get_warehouse(db, warehouse_id)
    if not warehouse:
        return False
    db.delete(warehouse)
    db.commit()
    return True
