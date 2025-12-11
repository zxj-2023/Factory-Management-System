from fastapi import APIRouter, Depends
from services.auth_deps import get_current_app_user

router = APIRouter(
    prefix="/factory",
    tags=["factory"],
    dependencies=[Depends(get_current_app_user)],
)

# 预留：工厂系统相关接口在此模块下实现
