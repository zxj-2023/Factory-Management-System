# seed_data.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from models import Base, Warehouse, Part, Supplier, Staff, Inventory, Purchase

# 数据库连接（替换为你的实际 URL）
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/factory_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # 1. 库房
        warehouses = [
            Warehouse(warehouse_id='W01', address='北京市海淀区中关村1号仓库'),
            Warehouse(warehouse_id='W02', address='上海市浦东新区张江2号仓库'),
            Warehouse(warehouse_id='W03', address='深圳市南山区科技园3号仓库'),
        ]
        db.add_all(warehouses)

        # 2. 零件
        parts = [
            Part(part_id='P1001', name='深沟球轴承', unit_price=25.50, type='轴承'),
            Part(part_id='P1002', name='圆柱滚子轴承', unit_price=45.00, type='轴承'),
            Part(part_id='P2001', name='渐开线齿轮', unit_price=18.75, type='齿轮'),
            Part(part_id='P2002', name='行星齿轮组', unit_price=88.00, type='齿轮'),
            Part(part_id='P3001', name='液压密封圈', unit_price=5.20, type='密封件'),
        ]
        db.add_all(parts)

        # 3. 供应商
        suppliers = [
            Supplier(supplier_id='S101', name='北方轴承厂', address='哈尔滨市', phone='13800001111'),
            Supplier(supplier_id='S102', name='华东齿轮制造', address='苏州市', phone='13800002222'),
            Supplier(supplier_id='S103', name='南方密封科技', address='广州市', phone='13800003333'),
        ]
        db.add_all(suppliers)

        # 4. 职工
        staffs = [
            Staff(staff_id='ST01', name='张伟', gender='M', hire_date=date(2020, 3, 15), title='仓库主管', warehouse_id='W01'),
            Staff(staff_id='ST02', name='李娜', gender='F', hire_date=date(2021, 7, 22), title='仓管员', warehouse_id='W01'),
            Staff(staff_id='ST03', name='王强', gender='M', hire_date=date(2019, 11, 10), title='仓库主管', warehouse_id='W02'),
            Staff(staff_id='ST04', name='赵敏', gender='F', hire_date=date(2022, 1, 5), title='仓管员', warehouse_id='W02'),
            Staff(staff_id='ST05', name='刘洋', gender='M', hire_date=date(2021, 9, 18), title='仓库主管', warehouse_id='W03'),
            Staff(staff_id='ST06', name='陈雪', gender='F', hire_date=date(2023, 4, 12), title='仓管员', warehouse_id='W03'),
        ]
        db.add_all(staffs)

        # 5. 库存（初始为 0）
        inventories = [
            Inventory(warehouse_id='W01', part_id='P1001', stock_quantity=0),
            Inventory(warehouse_id='W01', part_id='P2001', stock_quantity=0),
            Inventory(warehouse_id='W02', part_id='P1002', stock_quantity=0),
            Inventory(warehouse_id='W02', part_id='P2002', stock_quantity=0),
            Inventory(warehouse_id='W03', part_id='P3001', stock_quantity=0),
            Inventory(warehouse_id='W01', part_id='P3001', stock_quantity=0),
        ]
        db.add_all(inventories)

        # 6. 采购记录
        purchases = [
            Purchase(purchase_id='PUR20250101001', part_id='P1001', supplier_id='S101', warehouse_id='W01', purchase_date=date(2025, 1, 1), quantity=100, actual_price=24.00),
            Purchase(purchase_id='PUR20250115002', part_id='P2001', supplier_id='S102', warehouse_id='W01', purchase_date=date(2025, 1, 15), quantity=200, actual_price=17.50),
            Purchase(purchase_id='PUR20250201003', part_id='P1002', supplier_id='S101', warehouse_id='W02', purchase_date=date(2025, 2, 1), quantity=80, actual_price=43.00),
            Purchase(purchase_id='PUR20250210004', part_id='P2002', supplier_id='S102', warehouse_id='W02', purchase_date=date(2025, 2, 10), quantity=50, actual_price=85.00),
            Purchase(purchase_id='PUR20250301005', part_id='P3001', supplier_id='S103', warehouse_id='W03', purchase_date=date(2025, 3, 1), quantity=1000, actual_price=5.00),
            Purchase(purchase_id='PUR20250305006', part_id='P3001', supplier_id='S103', warehouse_id='W01', purchase_date=date(2025, 3, 5), quantity=500, actual_price=5.00),
            Purchase(purchase_id='PUR20250310007', part_id='P1001', supplier_id='S101', warehouse_id='W01', purchase_date=date(2025, 3, 10), quantity=150, actual_price=23.80),
            Purchase(purchase_id='PUR20250320008', part_id='P2001', supplier_id='S102', warehouse_id='W01', purchase_date=date(2025, 3, 20), quantity=100, actual_price=17.80),
        ]
        db.add_all(purchases)

        # 7. 提交事务
        db.commit()
        print("✅ 样例数据插入成功！")

        # 8. 自动更新库存（应用层逻辑）
        update_inventory_from_purchases(db)

    except Exception as e:
        db.rollback()
        print(f"❌ 数据插入失败: {e}")
    finally:
        db.close()

def update_inventory_from_purchases(db):
    """根据采购记录更新库存"""
    from sqlalchemy import select, func
    # 按 (warehouse_id, part_id) 聚合采购数量
    purchase_agg = db.execute(
        select(
            Purchase.warehouse_id,
            Purchase.part_id,
            func.sum(Purchase.quantity).label('total_qty')
        ).group_by(Purchase.warehouse_id, Purchase.part_id)
    ).all()

    for wh_id, part_id, total_qty in purchase_agg:
        # 更新对应库存
        inv = db.execute(
            select(Inventory)
            .where(Inventory.warehouse_id == wh_id, Inventory.part_id == part_id)
        ).scalar_one_or_none()
        if inv:
            inv.stock_quantity += total_qty
    db.commit()
    print("✅ 库存已根据采购记录更新！")

if __name__ == "__main__":
    seed_data()