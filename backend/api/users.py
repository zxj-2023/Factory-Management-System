from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from schemas.user import UserOut, UserUpdate
from services import users as users_service
from services.auth_deps import get_current_app_user, require_app_roles
from src.db.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[
        Depends(get_current_app_user),
        Depends(require_app_roles("admin")),
    ],
)


@router.get("", response_model=List[UserOut])
def list_users(
    email: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    warehouse_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return users_service.list_users(db, email=email, role=role, warehouse_id=warehouse_id)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, payload: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = users_service.update_user(db, user_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
