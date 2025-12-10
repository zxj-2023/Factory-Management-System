# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个使用 FastAPI + React + Supabase 的工厂管理系统数据库项目。项目定义了工厂的零件管理、供应商、仓库、职工、库存和采购等核心业务模型。

## 核心数据模型

项目使用 SQLAlchemy ORM 定义了以下核心业务模型（在 [backend/src/db/models.py](backend/src/db/models.py) 中）：

- **Part** - 零件表（part_id, name, unit_price, type）
- **Supplier** - 供应商表（supplier_id, name, address, phone）
- **Warehouse** - 仓库表（warehouse_id, address）
- **Staff** - 职工表（staff_id, name, gender, hire_date, title, warehouse_id）
- **Inventory** - 库存表（warehouse_id, part_id, stock_quantity）- 复合主键
- **Purchase** - 采购表（purchase_id, part_id, supplier_id, warehouse_id, purchase_date, quantity, actual_price）

## Supabase 集成

项目已配置 Supabase MCP 服务器：

- 项目引用：`fswbnlfblhgnmjevlktk`
- 在进行任何数据库操作时，必须使用 MCP Supabase 工具

## 常用命令

### 环境设置

```bash
# 进入后端目录
cd backend

# 安装 Python 依赖
pip install sqlalchemy psycopg2-binary python-dotenv fastapi uvicorn

# 创建 .env 文件并设置 DATABASE_URL，例如：
# DATABASE_URL=postgresql://username:password@localhost:5432/factory_db
```

### 数据库操作（使用 Supabase）

```bash
# 进入后端目录
cd backend

# 查看当前数据库表
# 使用 mcp__supabase__list_tables

# 查看当前迁移
# 使用 mcp__supabase__list_migrations

# 创建新的迁移（DDL操作）
# 使用 mcp__supabase__apply_migration

# 执行 SQL 查询
# 使用 mcp__supabase__execute_sql
```

### 开发命令

```bash
# 启动 FastAPI 开发服务器（待实现）
uvicorn src.main:app --reload --port 8000

# 运行测试（待实现）
pytest

# 前端开发（待实现）
cd frontend
npm install
npm run dev
```

## 架构说明

### 数据库连接

- 使用 Supabase PostgreSQL 作为数据存储
- 通过 MCP 工具进行所有数据库操作
- 项目的 [models.py](backend/src/db/models.py) 定义了完整的数据结构

### 业务逻辑

- 库存管理：Inventory 表记录各仓库的零件库存数量
- 采购记录：Purchase 表记录采购详情，包含实际采购价格
- 数据完整性：通过 CheckConstraint 确保单价、数量等字段为正数
- 库存更新：根据采购记录聚合更新库存

### FastAPI 后端架构

```
backend/
├── src/
│   ├── db/                     # 数据库模型和操作
│   │   ├── models.py          # SQLAlchemy 模型
│   │   ├── create_tables.py   # 表创建脚本
│   │   └── seed_data.py       # 初始化数据
│   ├── auth/                  # 认证模块（待实现）
│   └── main.py                # FastAPI 应用入口（待实现）
├── api/                       # API 路由（待实现）
├── services/                  # 业务服务层（待实现）
└── tests/                     # 测试文件（待实现）
```

### React 前端架构（待实现）

```
frontend/
├── src/
│   ├── components/            # React 组件
│   ├── pages/                 # 页面组件
│   ├── services/              # API 调用服务
│   ├── hooks/                 # 自定义 hooks
│   └── utils/                 # 工具函数
├── public/                    # 静态资源
└── package.json               # 依赖配置
```

## 注意事项

1. **必须使用 Supabase MCP 工具**进行所有数据库操作，不要直接使用 SQLAlchemy 连接
2. Inventory 表使用复合主键 (warehouse_id, part_id)
3. Staff.gender 字段限制为 'M' 或 'F'
4. 所有价格相关字段使用 DECIMAL 类型确保精度
5. 采购记录中的 actual_price 可能与 Part.unit_price 不同，反映实际采购价格
6. 项目结构符合 FastAPI 和 React 最佳实践

## 待实现功能

1. FastAPI 后端 API 实现
2. React 前端界面开发
3. 认证和授权系统
4. 库存预警功能
5. 数据报表和统计
6. 单元测试和集成测试