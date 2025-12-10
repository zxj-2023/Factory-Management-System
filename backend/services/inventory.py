"""
库存（inventory）服务层：封装库存的查询、创建、更新、调整等操作。
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from schemas.inventory import InventoryAdjust, InventoryCreate, InventoryUpdate
from src.db import models


def list_inventory(db: Session, warehouse_id: Optional[str] = None, part_id: Optional[str] = None) -> List[models.Inventory]:
    query = db.query(models.Inventory)
    if warehouse_id:
        query = query.filter(models.Inventory.warehouse_id == warehouse_id)
    if part_id:
        query = query.filter(models.Inventory.part_id == part_id)
    return query.all()


def get_inventory(db: Session, warehouse_id: str, part_id: str) -> Optional[models.Inventory]:
    return (
        db.query(models.Inventory)
        .filter(
            models.Inventory.warehouse_id == warehouse_id,
            models.Inventory.part_id == part_id,
        )
        .first()
    )


def create_inventory(db: Session, payload: InventoryCreate) -> models.Inventory:
    record = models.Inventory(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_inventory(db: Session, warehouse_id: str, part_id: str, payload: InventoryUpdate) -> Optional[models.Inventory]:
    record = get_inventory(db, warehouse_id, part_id)
    if not record:
        return None
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


def adjust_inventory(db: Session, warehouse_id: str, part_id: str, payload: InventoryAdjust) -> Optional[models.Inventory]:
    record = get_inventory(db, warehouse_id, part_id)
    if not record:
        return None
    new_qty = record.stock_quantity + payload.delta
    if new_qty < 0:
        return None
    record.stock_quantity = new_qty
    db.commit()
    db.refresh(record)
    return record


def delete_inventory(db: Session, warehouse_id: str, part_id: str) -> bool:
    record = get_inventory(db, warehouse_id, part_id)
    if not record:
        return False
    db.delete(record)
    db.commit()
    return True
