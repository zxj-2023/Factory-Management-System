# 外键字段前端选择策略（设计说明）

## 背景
后端已启用外键约束（采购关联零件/供应商/仓库，库存关联仓库/零件等）。避免用户输入不存在的 ID，前端应通过「下拉选择」或「级联选择」提供有效选项，并在提交前校验。

## 适用模块与外键
- 采购（purchase）：`part_id`、`supplier_id`、`warehouse_id`
- 库存（inventory）：`warehouse_id`、`part_id`
- 员工（staff）：`warehouse_id`（可空）
- 其他：如后续新增关联字段，沿用同一模式

## 接口与数据加载
1. 启动页面或打开「新增/编辑」弹窗时，直接加载全部外键选项（数据量小可一次性取全）：
   - `/factory/parts` → 零件列表（id、name、unit_price）
   - `/factory/suppliers` → 供应商列表（id、name、contact）
   - `/factory/warehouses` → 仓库列表（id、name、location）
2. 缓存策略：保持在页面 state 即可，数据量小无需分页/搜索；切换页面时再刷新，保证选项与后端同步。

## 前端表单交互
- 组件选择：AntD `Select`（单选）、`AutoComplete`（长列表搜索）或 `TreeSelect`（若需分组）。
- 展示字段：选项 label 使用业务含义（如「P001 - 螺母」），value 传递对应 id。
- 默认值：编辑时回填后端返回的外键 id；新增时为空。
- 验证：提交前检查必填外键非空；数量/价格为数值且非负。

## 提交与错误处理
- 提交：表单组装 payload 时直接使用选中的外键 id。
- 错误提示：若后端仍返回 FK 冲突（列表过期或被删除），捕获 400/409/500，提示「所选关联数据已不存在，请刷新列表后重试」并重新拉取选项。

## 后端辅助（可选）
- 当前数据量小，可直接使用完整列表；若未来增长，再考虑模糊查询或精简列表。

## 示例（前端调用约定）
- 采购弹窗打开：并行请求 `/factory/parts`, `/factory/suppliers`, `/factory/warehouses`，填充下拉。
- 新增采购提交：`POST /factory/purchases`，body 含 `part_id`, `supplier_id`, `warehouse_id`, `purchase_date`, `quantity`, `actual_price`。
- 出错重试：收到外键错误 → 重新加载选项 → 提示用户重新选择。
