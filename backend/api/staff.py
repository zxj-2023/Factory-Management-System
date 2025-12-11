"""
员工（staff）相关路由：CRUD，支持按仓库过滤。
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from schemas.staff import StaffCreate, StaffOut, StaffUpdate
from services import staff as staff_service
from services.auth_deps import get_current_app_user, require_app_roles
from src.db.database import get_db

router = APIRouter(
    prefix="/factory/staff",
    tags=["staff"],
    dependencies=[Depends(get_current_app_user)],
)


@router.get("", response_model=List[StaffOut])
def list_staff(warehouse_id: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return staff_service.list_staff(db, warehouse_id)


@router.get("/{staff_id}", response_model=StaffOut)
def get_staff(staff_id: str, db: Session = Depends(get_db)):
    staff = staff_service.get_staff(db, staff_id)
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    return staff


@router.post(
    "",
    response_model=StaffOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_app_roles("admin", "warehouse_manager"))],
)
def create_staff(payload: StaffCreate, db: Session = Depends(get_db)):
    return staff_service.create_staff(db, payload)


@router.put(
    "/{staff_id}",
    response_model=StaffOut,
    dependencies=[Depends(require_app_roles("admin", "warehouse_manager"))],
)
def update_staff(staff_id: str, payload: StaffUpdate, db: Session = Depends(get_db)):
    staff = staff_service.update_staff(db, staff_id, payload)
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    return staff


@router.delete(
    "/{staff_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_app_roles("admin", "warehouse_manager"))],
)
def delete_staff(staff_id: str, db: Session = Depends(get_db)):
    ok = staff_service.delete_staff(db, staff_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    return None
