# 前端集成 Supabase Auth（实施思路）

## 目标
- 前端使用 Supabase Auth 完成登录/注册，获取 access token（JWT）。
- JWT 通过 `Authorization: Bearer <token>` 传给后端 FastAPI，后端依赖 `get_current_user`/`require_roles` 做鉴权。
- 角色信息从 Supabase JWT 的 `role` 或 `app_metadata/user_metadata` 中读取，与后端四类角色映射。

## 准备工作
- 依赖：`@supabase/supabase-js`（若未装）。
- 环境变量（前端）：
  - `REACT_APP_SUPABASE_URL=<project>.supabase.co`
  - `REACT_APP_SUPABASE_ANON_KEY=<publishable/anon key>`（勿用 service_role）。
- 创建客户端（示例：`src/services/supabaseClient.ts`）：
  ```ts
  import { createClient } from '@supabase/supabase-js'

  const supabaseUrl = process.env.REACT_APP_SUPABASE_URL!
  const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY!

  export const supabase = createClient(supabaseUrl, supabaseKey)
  ```

## 基本流程
- 注册：`supabase.auth.signUp({ email, password, options: { emailRedirectTo } })`。
- 登录：`supabase.auth.signInWithPassword({ email, password })`。
- 登出：`supabase.auth.signOut()`。
- 会话获取：`supabase.auth.getSession()`（页面加载时）或 `onAuthStateChange` 监听并同步到全局状态（Redux/Context）。
- 将 access token 传给后端：在请求拦截器里读取 `session.access_token`，设置 `Authorization: Bearer <token>`。

## 角色与后端对接
- 登录后从 JWT 的 `user`/`session` 中读取 `role` 或自定义的 `user_metadata/app_metadata.roles`，存到前端全局状态，用于前端菜单/路由控制。
- 后端仍以自身 `require_roles` 为准，前端只做“体验层”控制。

## 页面/组件建议
- Auth 表单组件：邮箱+密码登录/注册；加载态/错误提示。
- 路由守卫：若无 session 则跳转登录页；根据角色隐藏不允许的入口。
- 个人中心：展示当前用户信息，支持退出/重取 token。

## 常见注意事项
- 仅在前端使用 anon/publishable key，不暴露 service_role。
- 若启用邮件验证，`emailRedirectTo` 必须在 Supabase 控制台的 Redirect URLs 中配置。
- 刷新页需重新获取 session（`getSession`），否则丢失登录态。
- OAuth/短信等高级登录可后续扩展，基础邮箱+密码先跑通。

## 与后端的约定
- 后端所有受保护接口需要 `Authorization: Bearer <access_token>`。
- 后端解析 JWT 并做角色判断；前端无需重复验签，只要传递 token。
- 如果角色字段存放在 metadata，需在登录后解析 `session.user.app_metadata` 或 `user_metadata`，与后端约定一致。