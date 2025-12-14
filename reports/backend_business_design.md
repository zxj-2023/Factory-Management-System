# 业务功能设计与实现（后端）

> 只讲业务逻辑与数据访问，不展开鉴权细节。

## 1. 技术栈与设计原则
- 框架：FastAPI（路由/依赖）、SQLAlchemy ORM（数据访问）、Pydantic v2（from_attributes 输出）。
- 数据库：Supabase Postgres，DDL 与 ORM 同步维护于 `backend/src/db`，保留复合主键、Check 约束、DECIMAL 精度。
- 事务：每请求 1 个 Session，写操作显式 `commit`，异常自动回滚，避免跨请求共享会话。
- 分层：路由层仅解析请求/组合依赖；服务层封装业务校验与 ORM；Schema 控制输入输出字段。

## 2. 路由与模块职责（业务向）
- `/users`（admin 专用）：业务用户列表与更新，`email` 只读，可修改 `display_name/role/warehouse_id`，用于分配角色与仓库权限。
- `/factory/parts`：零件主数据增删改查，校验 `unit_price >= 0`，描述字段可选。
- `/factory/suppliers`：供应商增删改查，联系方式与地址可选。
- `/factory/warehouses`：仓库增删改查，名称唯一约束于应用侧，address 可选。
- `/factory/staff`：员工增删改查，`gender` 仅允许 `M/F`，`hire_date` 为日期类型，关联 `warehouse_id` 可空。
- `/factory/inventory`：仓库-零件库存，复合主键 `(warehouse_id, part_id)`；支持创建、更新数量、删除；数量使用 DECIMAL/NUMERIC 避免精度丢失。
- `/factory/purchases`：采购单增删改查，关联零件/供应商/仓库；`actual_price` 可与零件单价不同；`quantity`、`actual_price` 均需非负。

## 3. 服务层实现要点
- 读取：统一 `list_*` 返回 ORM 对象列表；`get_*` 按 id/复合键查询并在不存在时抛 404。
- 创建：Pydantic Create 模型转为 ORM，必要时先校验外键存在（如采购需要零件、供应商、仓库存在）。
- 更新：`apply_update` 仅覆盖传入字段；更新后 `refresh` 返回最新数据；更新失败返回 404。
- 删除：先查再删，复合键（inventory）使用联合过滤条件。

示例（库存写入节选）：
```python
def upsert_inventory(db: Session, data: InventoryCreate):
    inv = db.query(Inventory).get((data.warehouse_id, data.part_id))
    if inv:
        inv.quantity = data.quantity
    else:
        inv = Inventory(**data.dict())
        db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv
```

## 4. 模型与约束
- 复合主键：`inventory (warehouse_id, part_id)` 确保同仓库同零件唯一。
- 枚举/Check：`staff.gender` 仅 `M/F`；`unit_price`、`actual_price`、`quantity` 非负 Check。
- 精度：价格与数量使用 DECIMAL/NUMERIC，避免浮点误差。
- 时间戳：所有表含 `created_at/updated_at`，由应用写入或数据库触发器维护。
- 业务用户表：`app_user(id, auth_user_id UUID, email, display_name, role, warehouse_id, created_at, updated_at)`；角色枚举 `admin/warehouse_manager/purchaser/inventory_operator`。

## 5. 典型业务流程
- 采购单创建：校验零件/供应商/仓库存在 → 非负价格/数量 → 写入 purchase → 返回记录。
- 库存写入/调整：依据 `(warehouse_id, part_id)` upsert；数量为 DECIMAL，防止精度损失；允许删除记录释放复合键。
- 员工维护：校验性别枚举、日期格式，`warehouse_id` 可选，更新时仅覆盖提供字段。
- 仓库/零件/供应商维护：常规 CRUD，删除前需应用层确保无业务依赖（未在 DB 级联）。
- 业务用户维护：管理员通过 `/users` 更新角色/仓库绑定，驱动后续接口的业务授权判断。

## 6. 运行与联调要点（后端视角）
- 环境变量：`DATABASE_URL`（必须）；其他 Supabase 相关变量用于上游鉴权，不影响纯业务 CRUD。
- 启动：`uvicorn backend.main:app --reload --port 8000`；数据库连通后可直接 CRUD。
- 种子数据：`backend/src/db/seed_data.py`（或 Supabase MCP 插入）提供仓库/零件/供应商/员工/库存/采购/业务用户示例，便于联调。
- DDL 与模型：`backend/src/db/ddl_add_timestamps.sql` 记录表结构，修改表结构时先更新 DDL，再同步 ORM 模型与 Schema。
