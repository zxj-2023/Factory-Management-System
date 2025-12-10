# 工厂系统功能与接口设计（基于现有数据库结构）

前缀约定：业务路由挂载在 `/factory` 下（见 `backend/api/factory.py`）。所有数据库写操作通过服务层调用 Supabase MCP，遵循 AGENTS 约束，不直接用 ORM 迁移/DDL。

## 模块与核心功能
- 零件（part）：CRUD、按类型/价格区间查询。
- 供应商（supplier）：CRUD、按名称模糊搜索、供应商-零件关联视图（可选）。
- 仓库（warehouse）：CRUD、仓库基本信息查询。
- 员工（staff）：CRUD、按仓库查询员工，性别约束 M/F，入职日期等。
- 库存（inventory）：查询/调整库存（增加/减少），校验非负；按仓库或零件过滤。
- 采购（purchase）：记录采购单，校验数量/价格正数；按时间/仓库/供应商/零件过滤。
- 系统（system）：健康检查。

## 接口草案（未实现，待按需细化）

### 系统
- `GET /health`：存活探测。

### 零件 part
- `GET /factory/parts`：列表，支持过滤 `type`、价格区间、分页。
- `GET /factory/parts/{part_id}`：详情。
- `POST /factory/parts`：创建（字段：part_id, name, unit_price, type）。
- `PUT /factory/parts/{part_id}`：全量更新。
- `PATCH /factory/parts/{part_id}`：部分更新（可选）。
- `DELETE /factory/parts/{part_id}`：删除（如有库存/采购记录需业务约束）。

### 供应商 supplier
- `GET /factory/suppliers`：列表，支持名称模糊、分页。
- `GET /factory/suppliers/{supplier_id}`：详情。
- `POST /factory/suppliers`：创建（supplier_id, name, address, phone）。
- `PUT /factory/suppliers/{supplier_id}`：更新。
- `DELETE /factory/suppliers/{supplier_id}`：删除前校验关联采购记录。

### 仓库 warehouse
- `GET /factory/warehouses`：列表。
- `GET /factory/warehouses/{warehouse_id}`：详情。
- `POST /factory/warehouses`：创建。
- `PUT /factory/warehouses/{warehouse_id}`：更新。
- `DELETE /factory/warehouses/{warehouse_id}`：删除前校验关联库存/员工/采购。

### 员工 staff
- `GET /factory/staff`：列表，支持按仓库过滤、分页。
- `GET /factory/staff/{staff_id}`：详情。
- `POST /factory/staff`：创建（gender 仅 M/F，warehouse_id 必填）。
- `PUT /factory/staff/{staff_id}`：更新。
- `DELETE /factory/staff/{staff_id}`：删除。

### 库存 inventory（复合主键 warehouse_id + part_id）
- `GET /factory/inventory`：列表，支持按仓库或零件过滤。
- `GET /factory/inventory/{warehouse_id}/{part_id}`：详情。
- `POST /factory/inventory`：创建库存记录（需确保复合键唯一，stock_quantity 非负）。
- `PUT /factory/inventory/{warehouse_id}/{part_id}`：全量更新数量。
- `POST /factory/inventory/{warehouse_id}/{part_id}/adjust`：调整库存（delta 正/负；结果不得为负）。

### 采购 purchase
- `GET /factory/purchases`：列表，支持时间范围、仓库、供应商、零件过滤，分页。
- `GET /factory/purchases/{purchase_id}`：详情。
- `POST /factory/purchases`：创建采购单（quantity > 0，actual_price > 0）。
- `PUT /factory/purchases/{purchase_id}`：更新（需重新校验约束）。
- `DELETE /factory/purchases/{purchase_id}`：删除/作废（视业务约束）。

## 数据与约束要点
- 复合主键：`inventory (warehouse_id, part_id)`。
- 约束：`unit_price >= 0`，`stock_quantity >= 0`，`quantity > 0`，`actual_price > 0`，`gender in ('M','F')`。
- 时间戳：所有表有 `created_at`/`updated_at`，`updated_at` 由触发器自动更新。
- 价格字段保持 DECIMAL(10,2)，`actual_price` 可与 `unit_price` 不同。
- 数据库 DDL/DML 修改通过 Supabase MCP 执行，不直接用 ORM 迁移。

## 实现建议（后续可落实）
- 路由模块拆分：`backend/api/parts.py`、`suppliers.py`、`warehouses.py`、`staff.py`、`inventory.py`、`purchases.py`；在 `backend/main.py` 统一 `include_router`。
- 依赖注入：在 FastAPI 依赖中获取 DB（通过 MCP 封装的服务层，而非直连 ORM 执行 DDL）。
- 校验层：请求体用 Pydantic 模型校验业务约束（正数、枚举等）。
- 错误处理：对唯一键/约束错误返回 400/409，数据库连接/内部错误返回 500。

## 角色与权限（功能设计）
- 系统管理员（admin）：全量 CRUD；用户/角色管理；配置修改；可覆盖所有业务操作。
- 仓库主管（warehouse_manager）：管理仓库与库存（增删改查）；查看采购/零件信息；管理员工（同仓库范围）；拥有库存操作员的全部权限。
- 采购员（purchaser）：管理采购单（增改查、作废/删除按业务约束）；查看供应商/零件/库存。
- 库存操作员（inventory_operator）：库存查询与调整（增减库存、编辑库存记录）、查看仓库/零件信息。

### 路由-权限映射（示例）
- `parts`: admin/purchaser 可写；其他角色只读。
- `suppliers`: admin/purchaser 可写；其他角色只读。
- `warehouses`: admin/warehouse_manager 可写；其他角色只读。
- `staff`: admin/warehouse_manager 可写；其他角色只读。
- `inventory`: admin/warehouse_manager/inventory_operator 可写；其他角色只读。
- `purchases`: admin/purchaser 可写；其他角色只读。
- 系统健康检查：公开或最小权限。

> 实施时在路由上挂权限依赖（如 `require_roles`/`require_permissions`），严格最小化授权；审计需求可在中间件记录操作者与请求结果。
