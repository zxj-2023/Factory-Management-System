# 数据库结构说明（来自 backend/src/db/models.py）

## 表结构概览
- part：零件基础信息。
- supplier：供应商信息。
- warehouse：仓库信息。
- staff：员工信息，关联仓库。
- inventory：库存，复合主键 `(warehouse_id, part_id)`。
- purchase：采购记录，关联零件、供应商、仓库。

## 字段与约束

### part
- part_id (PK, String(20))：零件编号。
- name (String(100), not null)：零件名称。
- unit_price (DECIMAL(10,2), not null, `unit_price >= 0`)：单价，非负。
- type (String(50), not null)：零件类型/分类。
- created_at (timestamptz, default now())：创建时间。
- updated_at (timestamptz, default now(), 触发器自动更新)：更新时间。

### supplier
- supplier_id (PK, String(20))：供应商编号。
- name (String(100), not null)：供应商名称。
- address (String(200))：地址。
- phone (String(20))：电话。
- created_at (timestamptz, default now())：创建时间。
- updated_at (timestamptz, default now(), 触发器自动更新)：更新时间。

### warehouse
- warehouse_id (PK, String(20))：仓库编号。
- address (String(200), not null)：仓库地址。
- created_at (timestamptz, default now())：创建时间。
- updated_at (timestamptz, default now(), 触发器自动更新)：更新时间。

### staff
- staff_id (PK, String(20))：员工编号。
- name (String(50), not null)：姓名。
- gender (CHAR(1), 约束 `IN ('M','F')`)：性别，限定 M/F。
- hire_date (Date, not null)：入职日期。
- title (String(50))：职称/岗位。
- warehouse_id (FK -> warehouse.warehouse_id, not null)：所属仓库。
- created_at (timestamptz, default now())：创建时间。
- updated_at (timestamptz, default now(), 触发器自动更新)：更新时间。

### inventory
- warehouse_id (PK, FK -> warehouse.warehouse_id)：仓库编号，复合主键之一。
- part_id (PK, FK -> part.part_id)：零件编号，复合主键之一。
- stock_quantity (Integer, not null, `stock_quantity >= 0`)：库存数量，非负。
- created_at (timestamptz, default now())：创建时间。
- updated_at (timestamptz, default now(), 触发器自动更新)：更新时间。

### purchase
- purchase_id (PK, String(30))：采购单号。
- part_id (FK -> part.part_id, not null)：采购零件。
- supplier_id (FK -> supplier.supplier_id, not null)：供应商。
- warehouse_id (FK -> warehouse.warehouse_id, not null)：入库仓库。
- purchase_date (Date, not null)：采购日期。
- quantity (Integer, not null, `quantity > 0`)：采购数量，正数。
- actual_price (DECIMAL(10,2), not null, `actual_price > 0`)：实际采购单价，正数。
- created_at (timestamptz, default now())：创建时间。
- updated_at (timestamptz, default now(), 触发器自动更新)：更新时间。

## 触发器
- 统一触发函数 `set_updated_at`：在各表的 BEFORE UPDATE 触发器中刷新 `updated_at`。
- 已在 part、supplier、warehouse、staff、inventory、purchase 上创建对应触发器。

## 外键关系
- staff.warehouse_id → warehouse.warehouse_id：员工归属仓库。
- inventory.warehouse_id → warehouse.warehouse_id；inventory.part_id → part.part_id：库存记录绑定仓库与零件（复合主键）。
- purchase.part_id → part.part_id；purchase.supplier_id → supplier.supplier_id；purchase.warehouse_id → warehouse.warehouse_id：采购记录绑定零件、供应商、入库仓库。

## 重要说明
- 遵守 AGENTS 要求：数据库变更通过 Supabase MCP 执行，不直接用 ORM 建连迁移。
- `inventory` 使用复合主键 `(warehouse_id, part_id)`。
- `gender` 限定 `M/F`；价格字段保持 DECIMAL 精度；`actual_price` 可与 `unit_price` 不同。
