# MIS 报告

## 1. 功能介绍
- 认证鉴权：Supabase Auth（JWT），登录/注册、登出；后端按业务表角色校验（admin / warehouse_manager / purchaser / inventory_operator）。
- 用户权限管理：`/users` 列表与编辑，只有 admin 可访问，维护业务用户角色/仓库绑定。
- 基础主数据：零件、供应商、仓库、员工的增删改查，前端表格+弹窗编辑，后端 FastAPI `/factory/*` 路由。
- 库存管理：按仓库-零件维度查询/维护库存，支持新增、更新、删除记录。
- 采购管理：采购单的查询、新增、编辑、删除，关联零件、供应商、仓库。
- 数据示例：已种子数据（仓库/零件/供应商/员工/库存/采购/业务用户）便于联调。

### 功能 1：用户注册登录与鉴权
- 注册/登录：前端用 Supabase Auth（邮箱+密码）完成注册、登录，获得 access token（JWT）。
- 令牌传递：前端 Axios 拦截器在每次请求添加 `Authorization: Bearer <token>`。
- 后端校验：FastAPI 读取 Authorization 头，JWKS 校验 JWT，提取 `sub/email`。`/auth/sync` 会在业务表创建/同步 `app_user` 记录。
- 业务权限：写操作按 `app_user.role` 限定（admin/warehouse_manager/purchaser/inventory_operator），读操作需登录即可。
- 关键路由：`/auth/sync` 登录后同步业务用户；`/users`（仅 admin）分配角色/仓库；`/factory/*` 为各业务模块。

### 角色权限一览

| 模块/操作         | admin | warehouse_manager | purchaser | inventory_operator |
|------------------|:-----:|:-----------------:|:---------:|:------------------:|
| 零件 CRUD        |   ✓   |         –         |     ✓     |         –          |
| 供应商 CRUD      |   ✓   |         –         |     ✓     |         –          |
| 仓库 CRUD        |   ✓   |         ✓         |     –     |         –          |
| 员工 CRUD        |   ✓   |         ✓         |     –     |         –          |
| 库存 CRUD        |   ✓   |         ✓         |     –     |         ✓          |
| 采购 CRUD        |   ✓   |         –         |     ✓     |         –          |
| 用户权限（/users)|   ✓   |         –         |     –     |         –          |
| 读取（列表/详情）| 登录  |       登录         |    登录    |        登录         |

## 2. MIS 系统基本框架图
```
[前端 (React + AntD + Redux)]
    |-- Supabase JS 客户端 (Auth 登录/会话)
    |-- Axios 调用 /api/... (携带 access token)
             |
             v
[后端 (FastAPI)]
    |-- 鉴权依赖: get_current_user -> get_current_app_user -> require_app_roles
    |-- 业务路由: /factory/*, /users, /auth/sync
             |
             v
[数据库 / Supabase]
    |-- 业务表: app_user, part, supplier, warehouse, staff, inventory, purchase
    |-- JWKS / JWT 签名服务 (Supabase Auth)
```

- 开发代理：前端 `/api` 通过 CRA 代理转发到 `http://localhost:8000`，避免跨域。
- 部署建议：生产环境用反向代理统一域名，后端加载正确的 SUPABASE_* 环境变量。

## 3. 系统结构设计
- 前端层：React + Ant Design，路由守卫（Supabase 会话），Axios 拦截器自动附加 access token。各模块页面通过服务层调用后端 `/factory/*`、`/users` 接口。
- 网关/代理：开发环境 CRA proxy 将 `/api` 转发后端；生产建议 Nginx/反向代理统一域名，转发 `/api` 至 FastAPI。
- 服务层（后端）：FastAPI 路由按模块拆分；依赖层鉴权 (`get_current_user`) + 业务角色 (`get_current_app_user` + `require_app_roles`)；服务模块封装 ORM 操作。
- 数据访问：SQLAlchemy 操作 `part/supplier/warehouse/staff/inventory/purchase/app_user` 等表，触发器维护 `updated_at`；示例数据便于联调。
- 认证授权：Supabase Auth 签发 JWT（ES/RS 为主，兼容 HS）；后端 JWKS 验证并以业务表角色为准；首次登录 `/auth/sync` 同步业务用户。
- 后端项目结构（核心目录）：
  - `api/`: FastAPI 路由（factory 各模块、auth、users 等），按资源划分。
  - `services/`: 业务逻辑与鉴权依赖（`auth_deps`、各资源 CRUD 服务）。
  - `schemas/`: Pydantic 请求/响应模型（from_attributes 支持 ORM 输出）。
  - `src/db/`: SQLAlchemy 模型、数据库工具、DDL/示例数据说明。
  - `config/`: 业务配置与工厂实例常量。
- 前端项目结构（核心目录）：
  - `src/pages/`: 首页、登录/注册、用户管理、零件/供应商/仓库/员工/库存/采购等页面。
  - `src/components/`: 布局（侧边栏、页头）、受保护路由、通用表单/表格组件。
  - `src/services/`: Supabase 客户端、Axios 实例与后端 API 封装（统一附带 access token，处理 401/403）。
  - `src/store/`: 会话与角色信息的全局状态。
  - `src/types/`: 前后端共享类型定义，保持接口契约一致。
  - `src/setupProxy.js`: 开发环境代理 `/api` 转发至 `http://localhost:8000`。

## 4. 物理设计与实施
- 数据库选型：使用 Supabase Postgres（云托管），开启 SSL；通过 Supabase 控制台管理 JWT 密钥与 API 密钥。
- 模型与表：使用 SQLAlchemy ORM 映射业务表（app_user、part、supplier、warehouse、staff、inventory、purchase），保持 DECIMAL 精度、复合主键（inventory）、性别枚举约束等。
- 迁移/DDL：`backend/src/db` 中维护 DDL 与示例数据说明，变更优先写 DDL，再同步 ORM 模型；生产环境建议使用迁移工具或 Supabase migration。
- 连接管理：`database.py` 提供引擎与 SessionLocal，FastAPI 依赖注入 db 会话，保证请求级事务关闭。
- 鉴权与授权：Supabase Auth 签发 JWT（优先 ES256），后端 JWKS 校验；业务权限依据 app_user.role；接口依赖组合 `get_current_user` + `get_current_app_user` + `require_app_roles`。
- 前后端联调：前端 Axios 统一以 `/api` 代理转发，携带 Supabase access token，后端通过依赖解析并落库。

### 关键代码片段（后端会话与依赖）
```python
# backend/src/db/database.py
engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 典型路由依赖组合
@router.get("/parts", response_model=List[PartOut], dependencies=[Depends(get_current_app_user)])
def list_parts(db: Session = Depends(get_db)):
    return part_service.list_parts(db)
```

## 5. 后端项目结构（树状图）
```
backend/
├─ main.py                   # FastAPI 入口，挂载路由与中间件
├─ config/
│  └─ __init__.py            # 业务配置/工厂实例常量
├─ api/                      # 路由层（请求解析+依赖组合）
│  ├─ auth.py                # /auth/sync 等认证同步
│  ├─ users.py               # 用户权限管理（admin）
│  └─ factory/               # 工厂模块路由
│     ├─ parts.py
│     ├─ suppliers.py
│     ├─ warehouses.py
│     ├─ staff.py
│     ├─ inventory.py
│     └─ purchases.py
├─ services/                 # 业务逻辑与依赖
│  ├─ auth.py                # 业务用户同步/查询
│  ├─ auth_deps.py           # get_current_user / get_current_app_user / require_app_roles
│  └─ *.py                   # 各模块 CRUD 服务
├─ schemas/                  # Pydantic 请求/响应模型
│  └─ *.py                   # 与路由输出/输入匹配
├─ src/db/
│  ├─ database.py            # SQLAlchemy 引擎/Session 管理
│  ├─ models.py              # ORM 模型定义
│  ├─ create_tables.py
│  ├─ seed_data.py
│  ├─ ddl_add_timestamps.sql # DDL/示例数据文档
│  └─ USER_TABLE_DESIGN.md
└─ docs/                     # 设计、鉴权、接口文档
```
