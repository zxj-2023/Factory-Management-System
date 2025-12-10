# Supabase 鉴权适配 FastAPI 实现思路

## 目标
- 使用 Supabase Auth 签发的 JWT 作为后端鉴权凭证。
- 后端 FastAPI 校验 JWT（签名、iss、aud、exp），提取用户和业务角色，结合现有路由的 `require_roles` 进行授权。
- 角色映射：将 Supabase JWT 的 `role` 或自定义 `app_metadata/user_metadata` 中的角色字段映射到项目的 4 类角色：`admin`、`warehouse_manager`、`purchaser`、`inventory_operator`。

## 前置配置
- 环境变量：
  - `SUPABASE_PROJECT_URL=https://<project>.supabase.co`
  - `SUPABASE_JWKS_URL=https://<project>.supabase.co/auth/v1/.well-known/jwks.json`
  - （可选）`SUPABASE_ISS=https://<project>.supabase.co/auth/v1`
- 依赖：JWT 校验库（如 `python-jose` 或 `authlib`）。

## FastAPI 依赖与权限
- `get_current_user`: 从 `Authorization: Bearer <jwt>` 读取 token，基于 JWKS 校验签名和 `iss/aud/exp`，解析 `sub` 和角色字段，返回用户上下文。
- `require_roles(*roles)`: 校验当前用户是否具备任一所需角色，不满足返回 403。
- 在路由上添加依赖：写操作绑定相应角色，读操作可放宽到登录用户。

## 路由-角色示例
- parts/suppliers/purchases 写：`admin`、`purchaser`
- warehouses/staff/inventory 写：`admin`、`warehouse_manager`（库存操作再加 `inventory_operator`）
- 读：登录用户或按需放宽。

## 实施步骤
1) 前端登录/注册改用 Supabase Auth，拿到 access token（JWT）。
2) 后端新增 auth 依赖模块：
   - JWKS 远程获取与缓存。
   - 校验 `iss/aud/exp`、签名；解析 `sub`、角色字段。
3) 在各路由添加 `Depends(require_roles(...))`，保持业务逻辑在 service 层。
4) 配置环境变量，运行时通过 `Authorization: Bearer <jwt>` 调用接口。
5) 测试：
   - 正常登录 token 访问读/写接口。
   - 角色不足返回 403。
   - 过期/无效 token 返回 401。

## 安全与运维
- 不暴露 service_role key 于前端；后端也避免用它转发请求。
- JWKS 有缓存（边缘约 10 分钟）；轮换密钥时注意缓存失效。
- 全程 HTTPS，定期轮换签名密钥；如用共享密钥 HS256，请尽快迁移到非对称签名。

## 路由统一鉴权的实践说明
- 统一鉴权思路：在对应 `APIRouter` 上通过 `dependencies=[Depends(require_roles(...))]` 统一挂载鉴权依赖，这样该 router 下的所有接口都会先运行 `get_current_user`（解析/校验 JWT）和角色判断。业务服务层无需重复鉴权。
- 局部加严：对敏感写操作，可在具体接口上叠加更严格的 `require_roles(...)`，实现分级授权。
- 全局兜底（可选）：可在 FastAPI app 级添加全局依赖/中间件统一解析 JWT，将用户信息放入 `request.state`；路由再用 `require_roles` 进行角色校验。
- 不建议：在每个业务函数手写解析 JWT，这会导致耦合高且重复代码。应把 JWT 解析和角色校验集中在依赖/中间件层，业务代码只处理逻辑。