import uvicorn
from fastapi import FastAPI

from api.factory import router as factory_router
from api.health import router as health_router
from api.inventory import router as inventory_router
from api.parts import router as parts_router
from api.purchases import router as purchases_router
from api.staff import router as staff_router
from api.suppliers import router as suppliers_router
from api.warehouses import router as warehouses_router
from api.auth import router as auth_router

# FastAPI 应用实例，集中注册各业务路由。
app = FastAPI(title="Factory API")

# 路由注册
app.include_router(health_router)
app.include_router(factory_router)
app.include_router(parts_router)
app.include_router(suppliers_router)
app.include_router(warehouses_router)
app.include_router(staff_router)
app.include_router(inventory_router)
app.include_router(purchases_router)
app.include_router(auth_router)


def main() -> None:
    """启动 FastAPI 应用。"""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
