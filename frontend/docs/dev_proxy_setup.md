# 前端开发环境代理配置（CRA）

## 目标
- 开发模式下将前端请求转发到后端，避免跨域预检（CORS）。
- 前端仍使用同源路径（如 `/api`），由代理转发到后端 `http://localhost:8000`。

## 适用项目
- 本项目使用 Create React App（react-scripts）。

## 配置步骤
1) 在 `frontend/src` 目录下创建 `setupProxy.js`：
   ```js
   const { createProxyMiddleware } = require('http-proxy-middleware');

   module.exports = function (app) {
     app.use(
       '/api',
       createProxyMiddleware({
         target: 'http://localhost:8000', // 后端地址
         changeOrigin: true,
         pathRewrite: {
           '^/api': '', // 去掉前缀，前端请求 /api/users -> 后端 /users
         },
       })
     );
   };
   ```

2) 前端请求改为同源路径，基准路径设为 `/api`：
   - `.env` 中将 `REACT_APP_API_URL` 设为 `/api`（或直接在 axios 创建时用 `/api`）。
   - 例如 axios 初始化：`baseURL: process.env.REACT_APP_API_URL || '/api'`。

3) 重启前端开发服务器（`npm start`），代理生效。

## 注意事项
- 仅开发模式生效；生产部署需在反向代理/Nginx 等环境配置相同转发。
- 如需携带凭证（cookie），保留 `changeOrigin: true` 并根据需要配置 `secure`/`ws` 等选项。
- 若前后端路径不一致，可调整 `pathRewrite`。例如后端前缀是 `/api`，可删除 pathRewrite。