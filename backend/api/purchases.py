"""
采购（purchase）相关路由：查询、创建、更新、删除采购单。
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from schemas.purchase import PurchaseCreate, PurchaseOut, PurchaseUpdate
from services import purchases as purchases_service
from src.db.database import get_db

router = APIRouter(prefix="/factory/purchases", tags=["purchases"])


@router.get("", response_model=List[PurchaseOut])
def list_purchases(
    warehouse_id: Optional[str] = Query(None),
    supplier_id: Optional[str] = Query(None),
    part_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return purchases_service.list_purchases(db, warehouse_id, supplier_id, part_id)


@router.get("/{purchase_id}", response_model=PurchaseOut)
def get_purchase(purchase_id: str, db: Session = Depends(get_db)):
    record = purchases_service.get_purchase(db, purchase_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
    return record


@router.post("", response_model=PurchaseOut, status_code=status.HTTP_201_CREATED)
def create_purchase(payload: PurchaseCreate, db: Session = Depends(get_db)):
    return purchases_service.create_purchase(db, payload)


@router.put("/{purchase_id}", response_model=PurchaseOut)
def update_purchase(purchase_id: str, payload: PurchaseUpdate, db: Session = Depends(get_db)):
    record = purchases_service.update_purchase(db, purchase_id, payload)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
    return record


@router.delete("/{purchase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase(purchase_id: str, db: Session = Depends(get_db)):
    ok = purchases_service.delete_purchase(db, purchase_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")
    return None
