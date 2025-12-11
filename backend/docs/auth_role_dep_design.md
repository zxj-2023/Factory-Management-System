# 鉴权与角色依赖分层方案（更新）

## 目的
- 将 JWT 鉴权（身份校验）与业务角色授权分离，便于复用与路由级声明。
- 角色权威来自业务表 `app_user`，避免信任 JWT 内可被客户端伪造的角色。

## 依赖设计
- `get_current_user`：验证 Supabase JWT（JWKS/HS 兼容），返回基本信息（sub/email）。
- `get_current_app_user`：基于 `sub` 查/建 `app_user`，返回业务用户对象（含 role）。
- `require_app_roles(*roles)`：依赖 `get_current_app_user`，校验业务角色是否在允许列表，不满足返回 403。

## 路由级统一鉴权
- 在 `APIRouter` 上挂鉴权依赖：
  ```python
  router = APIRouter(
      prefix="/inventory",
      dependencies=[Depends(get_current_app_user)],  # 统一鉴权+取业务用户
  )
  ```
- 角色校验可按业务需求选择：
  - 路由级统一：`dependencies=[Depends(require_app_roles("admin","warehouse_manager"))]`
  - 接口级精细：在具体接口上单独 `Depends(require_app_roles(...))`。

## 何时路由统一，何时接口精细
- 鉴权：推荐路由级统一（所有接口都需登录）。
- 角色：若同一 router 下权限差异大，倾向接口级单独声明，避免覆盖/遗漏；若差异小可在路由级统一，再对个别接口叠加更严格依赖。

## 数据流
1) 客户端携带 `Authorization: Bearer <token>` 调用接口。
2) `get_current_user` 校验 JWT；`get_current_app_user` 用 `sub` 查/建 `app_user`（默认角色可配置）。
3) `require_app_roles` 校验业务角色；通过则进入业务逻辑，失败返回 403。

## 优点
- 权限声明集中可控，减少重复代码。
- 角色来源单一（业务表），安全性高。
- 易扩展：新增角色/路由只需调整依赖或声明。

## 实施建议
- 保持 `/auth/sync` 首登创建 `app_user`，默认角色设为最小权限。
- 鉴权依赖可路由级统一；角色依赖视业务颗粒度决定放路由级或接口级。