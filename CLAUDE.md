# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个使用 SQLAlchemy 的工厂管理系统数据库项目。项目定义了工厂的零件管理、供应商、仓库、职工、库存和采购等核心业务模型。

## 核心数据模型

项目包含以下主要的 SQLAlchemy 模型（在 models.py 中）：

- **Part** - 零件表（part_id, name, unit_price, type）
- **Supplier** - 供应商表（supplier_id, name, address, phone）
- **Warehouse** - 仓库表（warehouse_id, address）
- **Staff** - 职工表（staff_id, name, gender, hire_date, title, warehouse_id）
- **Inventory** - 库存表（warehouse_id, part_id, stock_quantity）- 复合主键
- **Purchase** - 采购表（purchase_id, part_id, supplier_id, warehouse_id, purchase_date, quantity, actual_price）

## 常用命令

### 环境设置

```bash
# 安装依赖（需要添加 sqlalchemy, psycopg2-binary, python-dotenv）
pip install sqlalchemy psycopg2-binary python-dotenv

# 创建 .env 文件并设置 DATABASE_URL，例如：
# DATABASE_URL=postgresql://username:password@localhost:5432/factory_db
```

### 数据库操作

```bash
# 创建所有数据表
python create_tables.py

# 插入初始化数据
python seed_data.py

# 运行主程序
python main.py
```

## 架构说明

### 数据库连接

- 使用 SQLAlchemy ORM 和 psycopg2 连接 PostgreSQL 数据库
- DATABASE_URL 通过环境变量设置，create_tables.py 使用 dotenv 加载
- seed_data.py 中硬编码了连接字符串，需要统一改为环境变量

### 业务逻辑

- 库存管理：Inventory 表记录各仓库的零件库存数量
- 采购记录：Purchase 表记录采购详情，包含实际采购价格
- 数据完整性：通过 CheckConstraint 确保单价、数量等字段为正数
- 库存更新：seed_data.py 中的 update_inventory_from_purchases() 函数根据采购记录聚合更新库存

### 注意事项

- Inventory 表使用复合主键 (warehouse_id, part_id)
- Staff.gender 字段限制为 'M' 或 'F'
- 所有价格相关字段使用 DECIMAL 类型确保精度
- 采购记录中的 actual_price 可能与 Part.unit_price 不同，反映实际采购价格

## MCP 配置

项目配置了 Supabase MCP 服务器，项目引用：fswbnlfblhgnmjevlktk

## 我的要求

1. 数据库使用supabase，在有关数据库的代码时，需要使用supabase，请调用mcp工具
2. 后端使用fastapi，前端使用react
3. 项目结构要清晰符合规范
