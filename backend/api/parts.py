"""
零件（part）相关路由：CRUD 及按类型筛选。
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from schemas.part import PartCreate, PartOut, PartUpdate
from services import parts as parts_service
from services.auth_deps import get_current_app_user, require_app_roles
from src.db.database import get_db

router = APIRouter(
    prefix="/factory/parts",
    tags=["parts"],
    dependencies=[Depends(get_current_app_user)],
)


@router.get("", response_model=List[PartOut])
def list_parts(part_type: Optional[str] = Query(None, alias="type"), db: Session = Depends(get_db)):
    return parts_service.list_parts(db, part_type)


@router.get("/{part_id}", response_model=PartOut)
def get_part(part_id: str, db: Session = Depends(get_db)):
    part = parts_service.get_part(db, part_id)
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Part not found")
    return part


@router.post(
    "",
    response_model=PartOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_app_roles("admin", "purchaser"))],
)
def create_part(payload: PartCreate, db: Session = Depends(get_db)):
    return parts_service.create_part(db, payload)


@router.put(
    "/{part_id}",
    response_model=PartOut,
    dependencies=[Depends(require_app_roles("admin", "purchaser"))],
)
def update_part(part_id: str, payload: PartUpdate, db: Session = Depends(get_db)):
    part = parts_service.update_part(db, part_id, payload)
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Part not found")
    return part


@router.delete(
    "/{part_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_app_roles("admin", "purchaser"))],
)
def delete_part(part_id: str, db: Session = Depends(get_db)):
    ok = parts_service.delete_part(db, part_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Part not found")
    return None
