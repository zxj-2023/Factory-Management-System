# Factory Management System

## 简介
FastAPI + Supabase 后端，React + Ant Design 前端的工厂管理系统。包含零件、供应商、仓库、员工、库存、采购、用户权限等模块，支持 Supabase Auth 鉴权和业务角色控制。

## 目录结构
- backend/
  - main.py：FastAPI 入口，注册各路由
  - api/：业务路由（factory 模块、auth、users 等）
  - services/：业务服务、鉴权依赖
  - schemas/：Pydantic 模型
  - src/db/：SQLAlchemy 模型、数据库工具、DDL/示例数据文档
  - docs/：后端设计文档
- frontend/
  - src/index.tsx, App.tsx：前端入口
  - src/components/Layout.tsx：主布局
  - src/pages/：业务页面（parts/suppliers/warehouses/staff/inventory/purchases/users 等）
  - src/services/：API 客户端、Supabase 客户端、业务服务
  - src/types/：前端类型定义
  - docs/：前端开发代理等说明

## 环境配置
- 后端环境变量（backend/.env）：
  - DATABASE_URL
  - SUPABASE_JWKS_URL
  - SUPABASE_ISS
  - SUPABASE_AUD
  - SUPABASE_JWT_SECRET（可选，兼容旧 HS256）
- 前端环境变量（frontend/.env）：
  - REACT_APP_API_URL=/api（使用 CRA 开发代理）
  - REACT_APP_SUPABASE_URL
  - REACT_APP_SUPABASE_ANON_KEY

## 安装与启动
### 后端
```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate
uv sync   # 或 pip install -e .
python main.py
```

### 前端
```bash
cd frontend
npm install
npm start
```
- CRA 开发代理：`/api` -> `http://localhost:8000`（见 `src/setupProxy.js`）。

## 鉴权与权限
- Supabase Auth JWT：JWKS 验证（ES/RS），可选 HS 兼容。
- 依赖分层：`get_current_user` 校验 JWT；`get_current_app_user` 查/建业务用户；`require_app_roles` 按业务角色校验。
- `/auth/sync`：首次登录创建业务用户（默认最小角色）。
- 示例权限：
  - parts/suppliers/purchases 写：admin、purchaser
  - warehouses/staff 写：admin、warehouse_manager
  - inventory 写：admin、warehouse_manager、inventory_operator
  - `/users`：admin

## 示例数据
- 参考 `backend/docs/sample_data.md`，已通过 MCP 导入基础数据（仓库、零件、供应商、员工、库存、采购、业务用户）。

## 前端功能
- 页面：
  - 首页（欢迎页）
  - 零件/供应商/仓库/员工/库存/采购：表格展示，支持增删改查（调用后端 /factory/* 接口）
  - 用户权限：列表与编辑（调用 /users 接口，仅 admin）
  - 登录/注册（Supabase Auth），路由守卫 `ProtectedRoute`，退出登录按钮
- API 请求自动附带 Supabase access token；403 时提示权限不足。

## 代理与跨域
- 开发环境使用 CRA 代理，同源路径 `/api` 转发到后端，避免 CORS 预检。
- 生产需自行配置反向代理或调整前端 API 基地址。

## 注意
- 旧版 `backend/docs/auth_design.md` 已删除，鉴权设计见 `backend/docs/auth_role_dep_design.md`。
- 若使用旧 HS256 token，请配置 `SUPABASE_JWT_SECRET`；切到新 Signing Key 后仅 JWKS 验证即可。