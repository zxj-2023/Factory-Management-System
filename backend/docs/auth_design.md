# 认证与权限设计（草案）

## 目标
- 提供统一的登录/鉴权机制，生成携带角色的 JWT。
- 路由按角色/权限控制访问，满足四类角色：admin、warehouse_manager、purchaser、inventory_operator。

## 路由草案（auth）
- `POST /auth/login`：用户名密码登录，返回 access token（JWT），payload 含 `sub`、`roles`，可选 refresh token。
- `POST /auth/refresh`（可选）：用 refresh token 换新的 access token。
- `GET /auth/me`：基于当前 token 返回用户信息与角色，用于前端初始化。

## JWT 载荷建议
- `sub`: 用户唯一标识
- `roles`: 角色列表，例如 `["warehouse_manager"]`
- `exp`, `iat`, `iss`, `aud` 等标准字段

## FastAPI 依赖示例
- `get_current_user`: 解析/校验 JWT，返回用户与角色信息。
- `require_roles(*roles)`: 校验当前用户是否具备任一所需角色，不满足返回 403。
  ```python
  def require_roles(*allowed):
      def checker(user=Depends(get_current_user)):
          if not set(user.roles) & set(allowed):
              raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden")
          return user
      return checker
  ```

## 角色-路由对应（与业务设计一致）
- admin：全量写；可管理用户/角色（后续扩展）。
- warehouse_manager：仓库/员工/库存可写。
- purchaser：采购、供应商、零件可写。
- inventory_operator：库存可写。
- 其他访问默认只读或拒绝。

## 安全与配置
- 秘钥/过期时间/issuer 等放环境变量（如 `SECRET_KEY`、`ACCESS_TOKEN_EXPIRES`）；不要提交明文到仓库。
- 使用 HTTPS 传输；前后端约定 `Authorization: Bearer <token>`。
- 可加入中间件记录操作审计日志（用户、路径、时间、结果）。

## 实施顺序建议
1) 定义用户与角色数据源（临时内存/配置或数据库表，DB 操作通过 MCP）。
2) 实现 `/auth/login` 生成 JWT；添加 `get_current_user` 依赖。
3) 为各业务路由添加 `require_roles` 依赖（最小权限原则）。
4) 按需实现 refresh/注销；补充安全测试（过期、伪造、权限不足）。