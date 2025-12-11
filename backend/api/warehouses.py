"""
仓库（warehouse）相关路由：CRUD。
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.warehouse import WarehouseCreate, WarehouseOut, WarehouseUpdate
from services import warehouses as warehouses_service
from services.auth_deps import get_current_app_user, require_app_roles
from src.db.database import get_db

router = APIRouter(
    prefix="/factory/warehouses",
    tags=["warehouses"],
    dependencies=[Depends(get_current_app_user)],
)


@router.get("", response_model=List[WarehouseOut])
def list_warehouses(db: Session = Depends(get_db)):
    return warehouses_service.list_warehouses(db)


@router.get("/{warehouse_id}", response_model=WarehouseOut)
def get_warehouse(warehouse_id: str, db: Session = Depends(get_db)):
    warehouse = warehouses_service.get_warehouse(db, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    return warehouse


@router.post(
    "",
    response_model=WarehouseOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_app_roles("admin", "warehouse_manager"))],
)
def create_warehouse(payload: WarehouseCreate, db: Session = Depends(get_db)):
    return warehouses_service.create_warehouse(db, payload)


@router.put(
    "/{warehouse_id}",
    response_model=WarehouseOut,
    dependencies=[Depends(require_app_roles("admin", "warehouse_manager"))],
)
def update_warehouse(warehouse_id: str, payload: WarehouseUpdate, db: Session = Depends(get_db)):
    warehouse = warehouses_service.update_warehouse(db, warehouse_id, payload)
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    return warehouse


@router.delete(
    "/{warehouse_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_app_roles("admin", "warehouse_manager"))],
)
def delete_warehouse(warehouse_id: str, db: Session = Depends(get_db)):
    ok = warehouses_service.delete_warehouse(db, warehouse_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    return None
