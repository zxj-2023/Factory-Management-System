# 鉴权与角色依赖分层方案（更新）

## 目的
- 将 JWT 鉴权（身份校验）与业务角色授权分离，便于复用与路由级声明。
- 角色权威来自业务表 `app_user`，而非 JWT 内的 role 字段，避免客户端伪造。

## 依赖设计
- `get_current_user`：验证 Supabase JWT（JWKS/HS 兼容），返回基本信息（sub/email）。
- `get_current_app_user`：基于 `sub` 查/建 `app_user`，返回业务用户对象（含 role）。
- `require_app_roles(*roles)`：依赖 `get_current_app_user`，校验业务角色是否在允许列表，不满足返回 403。

## 路由级统一鉴权
- 在 `APIRouter` 上挂依赖，让该 router 下所有接口自动鉴权+取业务用户：
  ```python
  router = APIRouter(
      prefix="/inventory",
      dependencies=[Depends(get_current_app_user), Depends(require_app_roles("admin","warehouse_manager","inventory_operator"))],
  )
  ```
- 若需要更严格的接口，可在具体接口叠加 `Depends(require_app_roles("admin"))`。
- 公开接口（如 `/health`）不挂鉴权依赖。

## 数据流
1) 客户端携带 `Authorization: Bearer <token>` 调用接口。
2) `get_current_user` 校验 JWT；`get_current_app_user` 用 `sub` 查/建 `app_user`（默认角色可配置）。
3) `require_app_roles` 校验业务角色；通过则进入业务逻辑，失败返回 403。

## 优点
- 权限声明集中在路由层（router 级依赖），减少接口内重复代码。
- 角色来源单一（业务表），避免信任客户端可改的 JWT role。
- 易于扩展：新增角色/路由只需调整依赖或路由声明，不侵入业务逻辑。

## 实施建议
- 在 `auth_deps.py` 增加/完善 `get_current_app_user`、`require_app_roles`（基于 `app_user`）。
- 在业务 router 上统一挂鉴权与角色依赖；敏感接口可额外叠加更严格的 `require_app_roles`。
- 保持 `/auth/sync` 在首次登录时创建 `app_user`，默认角色设为最小权限。