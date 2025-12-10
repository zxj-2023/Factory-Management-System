# 用户业务表设计（User Profile）

## 目的
- 将 Supabase Auth 的用户（`sub` / `user.id`）与业务角色、档案信息绑定。
- 作为应用内角色的权威来源，避免仅依赖 JWT metadata。

## 表名与字段
- 表名：`app_user`（示例，可按需调整）
- 字段：
  - `id` (PK, UUID)：业务用户主键，推荐使用与 Supabase Auth `user.id` 对应，或单独 UUID 但需要字段存 Auth ID。
  - `auth_user_id` (UUID, unique, not null)：Supabase Auth 用户 ID，对应 JWT 的 `sub`。
  - `email` (varchar, not null)：用户邮箱（可与 Auth 保持一致）。
  - `display_name` (varchar, nullable)：显示名称。
  - `role` (varchar, not null)：业务角色，枚举之一：`admin` | `warehouse_manager` | `purchaser` | `inventory_operator`。
  - `warehouse_id` (varchar, nullable)：可选归属仓库（适用于仓库主管/库存操作员等）。
  - `created_at` (timestamptz, default now())
  - `updated_at` (timestamptz, default now(), on update now())

## 约束
- `auth_user_id` 唯一：确保一对一映射 Supabase Auth 用户。
- `role` 限定枚举（可用 CHECK 或业务层校验）：`role IN ('admin','warehouse_manager','purchaser','inventory_operator')`。
- 如需绑定仓库：`warehouse_id` 外键 -> `warehouse.warehouse_id`（可选）。

## 使用建议
- 登录后：根据 JWT 的 `sub` 查询 `app_user` 获取权威角色/信息。若不存在可触发首次注册逻辑（创建业务用户，默认角色由管理员或预设流程决定）。
- 前端展示：可从接口返回 `display_name`/`role`/`warehouse_id` 等；角色也可同步到 JWT metadata，但以表数据为准。
- 安全：不要在 `app_metadata/user_metadata` 放敏感信息；角色变更以此表为准并同步刷新客户端会话。

## 示例 DDL（PostgreSQL）
```sql
CREATE TABLE app_user (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auth_user_id UUID NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    role VARCHAR(30) NOT NULL,
    warehouse_id VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE app_user
    ADD CONSTRAINT check_app_user_role
    CHECK (role IN ('admin','warehouse_manager','purchaser','inventory_operator'));

-- 可选：绑定仓库
-- ALTER TABLE app_user
--   ADD CONSTRAINT fk_app_user_warehouse
--   FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id);

-- 触发器（若需要 updated_at 自动更新时间，可与现有 set_updated_at 复用）
-- CREATE TRIGGER trg_app_user_set_updated_at
--     BEFORE UPDATE ON app_user
--     FOR EACH ROW
--     EXECUTE FUNCTION set_updated_at();
```

> 注意：DDL 如需执行，请通过 Supabase MCP 迁移流程。表名/字段可按团队约定调整。
