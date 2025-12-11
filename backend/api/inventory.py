"""
库存（inventory）相关路由：查询、创建、更新、调整库存。
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from schemas.inventory import InventoryAdjust, InventoryCreate, InventoryOut, InventoryUpdate
from services import inventory as inventory_service
from services.auth_deps import get_current_app_user, require_app_roles
from src.db.database import get_db

router = APIRouter(
    prefix="/factory/inventory",
    tags=["inventory"],
    dependencies=[Depends(get_current_app_user)],
)


@router.get("", response_model=List[InventoryOut])
def list_inventory(
    warehouse_id: Optional[str] = Query(None),
    part_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return inventory_service.list_inventory(db, warehouse_id, part_id)


@router.get("/{warehouse_id}/{part_id}", response_model=InventoryOut)
def get_inventory(warehouse_id: str, part_id: str, db: Session = Depends(get_db)):
    record = inventory_service.get_inventory(db, warehouse_id, part_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    return record


@router.post(
    "",
    response_model=InventoryOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_app_roles("admin", "warehouse_manager", "inventory_operator"))],
)
def create_inventory(payload: InventoryCreate, db: Session = Depends(get_db)):
    return inventory_service.create_inventory(db, payload)


@router.put(
    "/{warehouse_id}/{part_id}",
    response_model=InventoryOut,
    dependencies=[Depends(require_app_roles("admin", "warehouse_manager", "inventory_operator"))],
)
def update_inventory(warehouse_id: str, part_id: str, payload: InventoryUpdate, db: Session = Depends(get_db)):
    record = inventory_service.update_inventory(db, warehouse_id, part_id, payload)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    return record


@router.post(
    "/{warehouse_id}/{part_id}/adjust",
    response_model=InventoryOut,
    dependencies=[Depends(require_app_roles("admin", "warehouse_manager", "inventory_operator"))],
)
def adjust_inventory(warehouse_id: str, part_id: str, payload: InventoryAdjust, db: Session = Depends(get_db)):
    record = inventory_service.adjust_inventory(db, warehouse_id, part_id, payload)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found or would become negative")
    return record


@router.delete(
    "/{warehouse_id}/{part_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_app_roles("admin", "warehouse_manager", "inventory_operator"))],
)
def delete_inventory(warehouse_id: str, part_id: str, db: Session = Depends(get_db)):
    ok = inventory_service.delete_inventory(db, warehouse_id, part_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    return None
