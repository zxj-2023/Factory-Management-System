from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.user import UserSyncOut
from services.auth import get_or_create_app_user
from services.auth_deps import get_current_user
from src.db.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/sync", response_model=UserSyncOut)
def sync_user(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    鉴权后，同步/返回业务用户信息。
    若不存在则创建一条业务用户记录（默认角色 inventory_operator）。
    """
    if not user.get("sub") or not user.get("email"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token payload")
    app_user = get_or_create_app_user(
        db=db,
        auth_user_id=user["sub"],
        email=user["email"],
        display_name=None,
    )
    return app_user
