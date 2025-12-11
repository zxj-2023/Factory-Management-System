"""
供应商（supplier）相关路由：CRUD 及名称模糊查询。
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from schemas.supplier import SupplierCreate, SupplierOut, SupplierUpdate
from services import suppliers as suppliers_service
from services.auth_deps import get_current_app_user, require_app_roles
from src.db.database import get_db

router = APIRouter(
    prefix="/factory/suppliers",
    tags=["suppliers"],
    dependencies=[Depends(get_current_app_user)],
)


@router.get("", response_model=List[SupplierOut])
def list_suppliers(name: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return suppliers_service.list_suppliers(db, name)


@router.get("/{supplier_id}", response_model=SupplierOut)
def get_supplier(supplier_id: str, db: Session = Depends(get_db)):
    supplier = suppliers_service.get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return supplier


@router.post(
    "",
    response_model=SupplierOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_app_roles("admin", "purchaser"))],
)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    return suppliers_service.create_supplier(db, payload)


@router.put(
    "/{supplier_id}",
    response_model=SupplierOut,
    dependencies=[Depends(require_app_roles("admin", "purchaser"))],
)
def update_supplier(supplier_id: str, payload: SupplierUpdate, db: Session = Depends(get_db)):
    supplier = suppliers_service.update_supplier(db, supplier_id, payload)
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return supplier


@router.delete(
    "/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_app_roles("admin", "purchaser"))],
)
def delete_supplier(supplier_id: str, db: Session = Depends(get_db)):
    ok = suppliers_service.delete_supplier(db, supplier_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return None
