# DB 变更流程（Supabase MCP）

## 使用场景
当修改 `backend/src/db/models.py`（新增字段、调整约束等）后，需让数据库结构同步，且遵循“仅通过 Supabase MCP 工具操作数据库”的要求。

## 推荐步骤
1) **梳理模型改动**：列出新增/修改/删除的字段或约束，留意精度要求（价格类字段保持 DECIMAL）。
2) **评估影响**：检查是否涉及复合主键、唯一约束、外键；确认数据迁移/回填需求（默认值、NOT NULL、历史数据处理）。
3) **编写迁移 SQL**：基于改动写 `ALTER TABLE ...` 等 DDL，命名约束（如 `check_price_positive`），避免使用 ORM `create_all` 直接建表。
4) **通过 Supabase MCP 应用**：使用 MCP 的迁移/SQL 执行能力提交迁移（如 `mcp__supabase__apply_migration`），确保先跑在开发/测试库再上生产。
5) **数据处理**：如需回填，编写对应 DML（`UPDATE`/`INSERT`），同样通过 MCP 执行。
6) **验证**：运行相关后端测试（pytest）或最小化查询确认：约束生效、默认值正确、读写正常。
7) **记录**：在 PR/说明中备注迁移内容、环境变量/依赖变更、测试结果。

## 注意事项
- ORM 侧重映射与读写，空库初建可用 `create_all`，但有现存数据/约束后，结构变更应以显式 DDL（迁移脚本）完成，并通过 MCP 执行。
- 不直接用 SQLAlchemy 连接真实库做迁移；保持 FastAPI/React 职责边界。
- 避免破坏已有主键/唯一约束；对 NOT NULL 新列先加默认或分批回填再收紧约束。
- 如需撤销，准备对称的回滚 SQL，并在 MCP 中谨慎执行。