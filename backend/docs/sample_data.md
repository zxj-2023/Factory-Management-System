# 示例数据（app_user/warehouse/part/supplier/staff/inventory/purchase）

## app_user（业务用户）
- auth_user_id: f8fa905a-2af8-4315-a331-92ad962ff689, email: z@demo.com, role: admin
- auth_user_id: 11111111-1111-1111-1111-111111111111, email: manager@demo.com, role: warehouse_manager, warehouse_id: W-001
- auth_user_id: 22222222-2222-2222-2222-222222222222, email: purchaser@demo.com, role: purchaser
- auth_user_id: 33333333-3333-3333-3333-333333333333, email: operator@demo.com, role: inventory_operator, warehouse_id: W-001

## warehouse
- W-001, 上海浦东仓
- W-002, 北京亦庄仓

## part
- P-001, 螺丝, 紧固件, 0.50
- P-002, 轴承, 传动件, 12.30

## supplier
- S-001, 华东五金, 上海, 13800000000
- S-002, 北方机电, 北京, 13900000000

## staff
- E-001, 张三, M, 2024-01-01, 仓库主管, W-001
- E-002, 李四, F, 2024-02-01, 库存操作员, W-002

## inventory
- (W-001, P-001) stock 1200
- (W-002, P-002) stock 300

## purchase
- PO-001, part P-001, supplier S-001, warehouse W-001, 2024-05-01, qty 100, price 0.48
- PO-002, part P-002, supplier S-002, warehouse W-002, 2024-05-02, qty 50, price 12.00