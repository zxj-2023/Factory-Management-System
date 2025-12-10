# 工厂管理系统 - 前端

使用 React + TypeScript + Ant Design 构建的现代化工厂管理系统前端。

## 技术栈

- **React 18** - 用户界面框架
- **TypeScript** - 类型安全的 JavaScript
- **Ant Design** - UI 组件库
- **Redux Toolkit** - 状态管理
- **React Router** - 路由管理
- **Axios** - HTTP 客户端

## 开发环境要求

- Node.js >= 16
- npm >= 8

## 快速开始

```bash
# 安装依赖
npm install

# 启动开发服务器
npm start

# 构建生产版本
npm run build
```

## 项目结构

```
src/
├── components/          # 通用组件
│   └── Layout.tsx      # 主布局组件
├── pages/              # 页面组件
│   ├── Dashboard.tsx   # 仪表板
│   ├── Parts.tsx       # 零件管理
│   ├── Suppliers.tsx   # 供应商管理
│   ├── Warehouses.tsx  # 仓库管理
│   ├── Staff.tsx       # 职工管理
│   ├── Inventory.tsx   # 库存管理
│   └── Purchases.tsx   # 采购记录
├── services/           # API 服务
│   └── api.ts         # Axios 配置
├── store/             # Redux 状态管理
│   └── index.ts       # Store 配置
├── types/             # TypeScript 类型定义
│   └── index.ts       # 通用类型
├── hooks/             # 自定义 React Hooks
└── utils/             # 工具函数
```

## 功能模块

- 📊 **仪表板** - 系统概览和关键指标
- 📦 **零件管理** - 零件信息的增删改查
- 🏢 **供应商管理** - 供应商信息管理
- 🏭 **仓库管理** - 仓库信息管理
- 👥 **职工管理** - 职工信息管理
- 📋 **库存管理** - 库存查询和管理
- 🛒 **采购记录** - 采购历史和记录

## 开发指南

### 添加新页面

1. 在 `pages/` 目录下创建新的页面组件
2. 在 `App.tsx` 中添加路由
3. 在 `Layout.tsx` 中添加菜单项

### API 调用示例

```typescript
import api from '../services/api';

// 获取所有零件
const getParts = async () => {
  const response = await api.get('/parts');
  return response.data;
};
```

### 状态管理

使用 Redux Toolkit 管理全局状态：

```typescript
// 创建 slice
import { createSlice } from '@reduxjs/toolkit';

const partSlice = createSlice({
  name: 'parts',
  initialState: [],
  reducers: {
    setParts: (state, action) => action.payload,
  },
});
```

## 部署

```bash
# 构建生产版本
npm run build

# 构建后的文件在 build/ 目录下
# 可以部署到任何静态文件服务器
```

## 环境变量

创建 `.env` 文件配置环境变量：

```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_TITLE=工厂管理系统
REACT_APP_DEBUG=true
```

## 注意事项

1. 所有 API 请求需要包含认证 token
2. 使用 TypeScript 确保类型安全
3. 遵循 Ant Design 设计规范
4. 保持代码整洁和组件复用
