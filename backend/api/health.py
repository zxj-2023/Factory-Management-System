from fastapi import APIRouter

router = APIRouter(prefix="", tags=["system"])


@router.get("/health")
async def health_check() -> dict:
    """
    健康检查：用于存活探测和基础连通性验证。
    """
    return {"status": "ok"}
