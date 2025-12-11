# 用户权限管理页面设计（前端需求）

## 目标
- 新增“用户权限管理”页面，读取 `app_user` 表的 `email`（不可改）、`display_name`、`role`（四种角色之一）、`warehouse_id`，支持查看与修改。
- 角色选项：`admin` / `warehouse_manager` / `purchaser` / `inventory_operator`。

## 后端接口（建议）
- `GET /users`：列表查询，返回 `id, email, display_name, role, warehouse_id, created_at`。
- `PUT /users/{id}`：更新 `display_name, role, warehouse_id`（email 不可改）。需权限：admin。
- 可选过滤：按 email/role/warehouse 查询，分页。

## 前端页面布局
- 路由：`/users`（受保护，需要 admin 权限）。
- 组件：表格 + 筛选 + 编辑弹窗。
  - 表格列：邮箱（只读）、显示名（可编辑）、角色（下拉）、仓库（输入/下拉）、创建时间。
  - 筛选：邮箱关键词、角色、仓库。
  - 编辑：点击“编辑”打开弹窗，提交调用 PUT。
  - 角色下拉固定四种选项；邮箱字段禁用。

## 数据流程
- 进入页面：调用 `GET /users` 获取列表，填充表格。
- 编辑提交：调用 `PUT /users/{id}`，成功后刷新列表。
- 权限：前端仅显示入口，后端以 `require_roles('admin')` 限制。

## 校验与约束
- email 不可修改。
- role 仅四种枚举；后端也应做校验。
- warehouse_id 可选；若与仓库表关联，建议后端校验存在性。

## 交互提示
- 更新成功/失败弹出 message。
- 更新时显示 loading 防重复提交。

> 注：需在后端实现对应的 `/users` 列表和更新接口，并在前端路由中添加 `/users` 页面与受保护的导航入口。