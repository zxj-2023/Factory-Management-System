# Repository Guidelines

## Project Structure & Modules

- `backend/` holds Python 3.12 code; `src/db/` contains the SQLAlchemy engine (`database.py`), declarative models, and helper scripts (`create_tables.py`, `seed_data.py`); `.env` stores `DATABASE_URL`.
- `frontend/` is a React + TypeScript app (Ant Design, Redux Toolkit); entry points are `src/index.tsx` and `src/App.tsx`, shared layout in `src/components/Layout.tsx`, feature pages under `src/pages/`, state in `src/store/`, API client in `src/services/api.ts`.
- `docs/` contains reference materials; `pyproject.toml` and `uv.lock` pin backend deps; `.venv/` is local-only.

## Setup, Build, and Run

- Backend deps: `python -m venv .venv && .venv\Scripts\activate && pip install -e .` (or `uv sync`).
- Configure `backend/.env` with `DATABASE_URL=postgresql://user:pass@host:5432/db` (SSL is enforced in `database.py`).
- Create tables: `python backend/src/db/create_tables.py`; seed sample data: `python backend/src/db/seed_data.py`; quick smoke: `python backend/main.py`.
- Frontend: `cd frontend && npm install && npm start` for dev; `npm run build` for production bundle.

## Coding Style & Naming

- Python: PEP 8, 4-space indent, favor type hints for new modules, keep environment keys UPPER_SNAKE_CASE; SQLAlchemy models use PascalCase classes and lowercase table names.
- TypeScript/React: follow CRA ESLint defaults; functional components; components/pages PascalCase file names, hooks prefixed with `use`, shared types in `src/types/`.
- Keep modules cohesive (db helpers in `backend/src/db/`, UI logic in page components, cross-cutting utilities in `frontend/src/services` or `src/store`).

## Testing Guidelines

- Frontend uses React Testing Library/Jest (via CRA); place `*.test.tsx` next to components; run `npm test` (optionally `CI=true npm test -- --watch=false`).
- Backend tests are open—add `pytest` cases under `backend/tests/test_*.py` for services, model constraints, and DB interactions (use a temp DB URL or fixtures to avoid mutating production data).
- Aim to cover new logic paths and critical DB constraints when modifying schemas or seed scripts.

## Commit and PR Guidelines

- Commit messages are short and imperative; mirror existing style (e.g., `react初始化`, `添加数据库模型`).
- PRs: include a concise summary, test commands/output, linked issues/tasks, and screenshots/GIFs for UI changes; call out schema or env var changes clearly.
- Keep backend and frontend changes scoped when possible; include migration/seed updates in the same PR as related model changes.

## Security and Configuration

- Do not commit `.env` or credentials; rotate `DATABASE_URL` if exposed.
- Use least-privilege DB roles for local testing; keep SSL settings enabled as in `database.py`.
- Document any new environment variables or required services in this file and `README.md`.

## 注意事项（Must-Know Notes）

- 数据库操作仅使用 Supabase MCP 工具，不直接通过 SQLAlchemy 建连。
- `inventory` 表使用复合主键 `(warehouse_id, part_id)`；`staff.gender` 仅允许 `M/F`。
- 所有价格字段保持 `DECIMAL` 精度，`purchase.actual_price` 可与 `part.unit_price` 不同。
- 维护 FastAPI + React 的目录和职责边界；依赖安装使用 `uv add`。

## 注意事项（Must-Know Notes）

- 数据库操作仅使用 Supabase MCP 工具，不直接通过 SQLAlchemy 建连。
- `inventory` 表使用复合主键 `(warehouse_id, part_id)`；`staff.gender` 仅允许 `M/F`。
- 所有价格字段保持 `DECIMAL` 精度，`purchase.actual_price` 可与 `part.unit_price` 不同。
- 维护 FastAPI + React 的目录和职责边界；依赖安装使用 `uv add`。
- 用中文回复我
