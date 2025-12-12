# Repository Guidelines

## Project Structure & Modules
- `backend/` holds Python 3.12 code; FastAPI app in `backend/main.py`; routes under `backend/api/`; business services under `backend/services/`; Pydantic schemas under `backend/schemas/`; DB models under `backend/src/db/models.py`.
- `frontend/` is React + TypeScript (CRA + Ant Design, Redux Toolkit); entry `src/index.tsx`, main layout `src/components/Layout.tsx`, pages under `src/pages/`, state in `src/store/`, API client in `src/services/api.ts`; Supabase client in `src/services/supabaseClient.ts`.
- `docs/` contains reference materials; backend uses `pyproject.toml` + `uv.lock`; `.venv/` local only.

## Setup, Build, Run
- Backend deps: `python -m venv .venv && .venv\Scripts\activate && uv sync` (or `pip install -e .`).
- Backend run: `python backend/main.py` (FastAPI with reload). Env: `DATABASE_URL`, `SUPABASE_JWKS_URL`, `SUPABASE_ISS`, `SUPABASE_AUD`, (optional) `SUPABASE_JWT_SECRET`.
- Frontend: `cd frontend && npm install && npm start`. Dev proxy: `/api` -> `http://localhost:8000`; set `REACT_APP_API_URL=/api`, `REACT_APP_SUPABASE_URL`, `REACT_APP_SUPABASE_ANON_KEY`.

## Coding Style & Naming
- Python: PEP 8, 4-space indent, type hints for new modules; SQLAlchemy models PascalCase classes, lowercase table names.
- TypeScript/React: CRA ESLint defaults; functional components; PascalCase files; hooks prefixed with `use`; shared types in `src/types/`.

## Testing Guidelines
- Frontend: React Testing Library/Jest; `*.test.tsx` next to components; run `npm test`.
- Backend: add pytest under `backend/tests/test_*.py` (if needed).

## Auth & Permissions
- Supabase Auth JWT via JWKS (ES/RS); optional HS fallback with `SUPABASE_JWT_SECRET` if old tokens exist.
- 鉴权与角色分层：`get_current_user` 验证 JWT；`get_current_app_user` 查/建业务用户；`require_app_roles` 基于业务表角色校验。建议路由级统一鉴权，角色可路由或接口级按需声明。
- `/auth/sync` 同步/创建业务用户（默认最小角色）。

## Factory API (示例权限)
- parts/suppliers/purchases 写：admin, purchaser；warehouses/staff 写：admin, warehouse_manager；inventory 写：admin, warehouse_manager, inventory_operator；读操作登录即可。

## Other Notes
- DB 操作通过 SQLAlchemy models；schema 变更/数据操作遵守 Supabase MCP 规定。
- Dev proxy 已配置 `frontend/src/setupProxy.js`；生产需自行配置反向代理。