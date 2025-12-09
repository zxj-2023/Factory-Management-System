# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个工厂管理系统，采用现代化的全栈架构：
- **后端**: FastAPI + SQLAlchemy + Supabase PostgreSQL
- **前端**: React (TypeScript)
- **数据库**: Supabase (PostgreSQL)
- **部署**: 生产就绪的云原生架构

## 项目结构

```
factory/
├── backend/                    # FastAPI 后端
│   └── src/
│       └── db/
│           ├── models.py       # SQLAlchemy 数据模型
│           ├── create_tables.py # 数据库表创建脚本
│           └── seed_data.py    # 示例数据脚本
├── frontend/                   # React 前端 (待创建)
├── .mcp.json                   # MCP 配置
├── .claude/                    # Claude 配置
└── pyproject.toml             # Python 项目配置
```

## 核心数据模型

项目使用 SQLAlchemy ORM 定义了以下核心业务模型：

### 1. **Part（零件）**
- `part_id`: 零件编号（主键）
- `name`: 零件名称
- `unit_price`: 单价（DECIMAL 精确计算）
- `type`: 零件类型

### 2. **Supplier（供应商）**
- `supplier_id`: 供应商编号（主键）
- `name`: 供应商名称
- `address`: 地址
- `phone`: 联系电话

### 3. **Warehouse（仓库）**
- `warehouse_id`: 仓库编号（主键）
- `address`: 仓库地址

### 4. **Staff（职工）**
- `staff_id`: 职工编号（主键）
- `name`: 姓名
- `gender`: 性别（M/F 约束）
- `hire_date`: 入职日期
- `title`: 职位
- `warehouse_id`: 所属仓库（外键）

### 5. **Inventory（库存）**
- 复合主键: `(warehouse_id, part_id)`
- `stock_quantity`: 库存数量（非负约束）

### 6. **Purchase（采购）**
- `purchase_id`: 采购单号（主键）
- `part_id`: 采购零件（外键）
- `supplier_id`: 供应商（外键）
- `warehouse_id`: 入库仓库（外键）
- `purchase_date`: 采购日期
- `quantity`: 采购数量（正值约束）
- `actual_price`: 实际采购价格（正值约束）

## 数据库配置

### Supabase 集成
- 项目已配置 Supabase MCP 服务器
- 项目引用: `fswbnlfblhgnmjevlktk`
- 使用 PostgreSQL 作为数据存储

### 环境变量
创建 `.env` 文件：
```
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]
```

## 常用命令

### 后端开发

```bash
# 进入后端目录
cd backend

# 安装 Python 依赖
pip install sqlalchemy psycopg2-binary python-dotenv fastapi uvicorn

# 创建数据库表
python src/db/create_tables.py

# 插入示例数据
python src/db/seed_data.py

# 启动 FastAPI 开发服务器
uvicorn src.main:app --reload --port 8000
```

### 前端开发（待实现）

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 业务逻辑说明

### 库存管理
- 库存通过 Inventory 表记录各仓库的零件库存
- 初始库存为 0，通过采购记录自动更新
- `seed_data.py` 中的 `update_inventory_from_purchases()` 函数聚合采购数量并更新库存

### 采购流程
- 每笔采购记录关联零件、供应商、仓库
- 支持实际采购价格与目录单价不同
- 所有采购都会自动增加对应仓库的库存

### 数据完整性
- 使用 CheckConstraint 确保数据合理性：
  - 单价、库存数量 >= 0
  - 采购数量、实际价格 > 0
  - 性别只能是 M/F
- 使用 DECIMAL 类型确保财务数据精度

## 开发指南

### 使用 Supabase
在处理数据库操作时，必须使用 MCP Supabase 工具：
- 查询数据：使用 `mcp__supabase__execute_sql`
- 创建表：使用 `mcp__supabase__apply_migration`
- 获取项目信息：使用 `mcp__supabase__get_project_url`

### API 设计原则
- 使用 FastAPI 创建 RESTful API
- 实现适当的 CRUD 操作
- 添加数据验证和错误处理
- 使用 Pydantic 模型定义请求/响应

### 前端开发原则
- 使用 TypeScript 确保类型安全
- 采用组件化架构
- 实现响应式设计
- 使用状态管理（如 Redux Toolkit）

## 待实现功能

1. **FastAPI 后端 API**
   - 零件管理 API
   - 供应商管理 API
   - 库存查询 API
   - 采购记录 API
   - 职工管理 API

2. **React 前端界面**
   - 登录/认证系统
   - 仪表板
   - 各实体的 CRUD 界面
   - 库存报表
   - 采购统计

3. **高级功能**
   - 库存预警
   - 采购建议
   - 数据导出
   - 批量操作

## 注意事项

- 所有数据库操作应通过 Supabase MCP 工具进行
- 保持前后端 API 接口的一致性
- 遵循 Python 和 JavaScript 的最佳实践
- 确保所有价格和数量计算的精确性
- 添加适当的日志记录和错误处理
