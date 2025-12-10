# 认证与权限设计（更新版）

## 目标
- 使用 Supabase Auth 签发的 JWT 作为统一凭证，不再自签本地 token。
- 路由按角色控制访问，满足四类角色：admin、warehouse_manager、purchaser、inventory_operator。
- JWT 校验与角色判断集中在依赖/中间件层，业务路由和服务层只处理业务逻辑。

## 登录与 Token 获取
- 前端/客户端通过 Supabase Auth 完成登录，获取 access token（JWT）。
- JWT 中的角色可放在 `role` 字段或 `app_metadata/user_metadata` 自定义字段，需与业务角色映射。

## 后端校验与依赖
- 环境：`SUPABASE_PROJECT_URL`、`SUPABASE_JWKS_URL`（`https://<project>.supabase.co/auth/v1/.well-known/jwks.json`）、可选 `SUPABASE_ISS`。
- `get_current_user`: 通过 JWKS 校验签名与 `iss/aud/exp`，解析 `sub` 和角色字段，返回用户上下文。
- `require_roles(*roles)`: 校验用户是否具备任一指定角色，不满足返回 403。
- 推荐在 `APIRouter` 上用 `dependencies=[Depends(require_roles(...))]` 做统一鉴权，敏感接口可再叠加更严格的 `require_roles`。

## 角色-路由对应（与业务设计一致）
- admin：全量写；可管理用户/角色（后续扩展）。
- warehouse_manager：仓库/员工/库存可写。
- purchaser：采购、供应商、零件可写。
- inventory_operator：库存可写。
- 其他访问默认只读或拒绝。

## 安全与配置
- 不暴露 service_role key 于前端；后端也避免用它转发请求。
- JWKS 有缓存（约 10 分钟）；轮换密钥时注意缓存失效。
- 全程 HTTPS，校验 `iss/aud/exp`，对无 token/过期/签名错误返回 401，对角色不足返回 403。
- 可加入中间件记录操作审计日志（用户、路径、时间、结果）。

## 实施顺序建议
1) 前端改用 Supabase Auth 登录，拿到 access token。
2) 后端实现 `get_current_user`（JWKS 校验 + 解析角色），实现 `require_roles`。
3) 在各业务路由挂 `require_roles`（router 级统一鉴权，必要时接口级加严）。
4) 补充安全测试：过期/伪造/角色不足场景。
