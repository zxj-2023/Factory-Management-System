import uvicorn
from fastapi import FastAPI

from api.factory import router as factory_router
from api.health import router as health_router

app = FastAPI(title="Factory API")

# 路由注册
app.include_router(health_router)
app.include_router(factory_router)


def main() -> None:
    """启动 FastAPI 应用。"""
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
