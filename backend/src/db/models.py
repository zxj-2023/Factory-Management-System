# models.py
from sqlalchemy import (
    create_engine, Column, String, Integer, DECIMAL, Date, CHAR,
    ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# SQLAlchemy 的基类，所有模型类都需要继承这个 Base
# declarative_base() 创建了一个基类，用于定义数据库表结构的映射
Base = declarative_base()

class Part(Base):
    __tablename__ = 'part'
    
    part_id = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    type = Column(String(50), nullable=False)
    
    # 约束：单价 >= 0
    __table_args__ = (
        CheckConstraint(unit_price >= 0, name='check_unit_price_positive'),
    )

class Supplier(Base):
    __tablename__ = 'supplier'
    
    supplier_id = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200))
    phone = Column(String(20))

class Warehouse(Base):
    __tablename__ = 'warehouse'
    
    warehouse_id = Column(String(20), primary_key=True)
    address = Column(String(200), nullable=False)

    # 可选：未来加组长时在此添加
    # leader_staff_id = Column(String(20), ForeignKey('staff.staff_id'), unique=True)

class Staff(Base):
    __tablename__ = 'staff'
    
    staff_id = Column(String(20), primary_key=True)
    name = Column(String(50), nullable=False)
    gender = Column(CHAR(1))
    hire_date = Column(Date, nullable=False)
    title = Column(String(50))
    warehouse_id = Column(String(20), ForeignKey('warehouse.warehouse_id'), nullable=False)
    
    # 约束：性别只能是 M/F
    __table_args__ = (
        CheckConstraint("gender IN ('M', 'F')", name='check_gender'),
    )

class Inventory(Base):
    __tablename__ = 'inventory'
    
    warehouse_id = Column(String(20), ForeignKey('warehouse.warehouse_id'), primary_key=True)
    part_id = Column(String(20), ForeignKey('part.part_id'), primary_key=True)
    stock_quantity = Column(Integer, nullable=False)
    
    # 表级约束：确保库存数量不能为负数
    # 当尝试插入或更新为负数时会触发数据库错误
    __table_args__ = (
        CheckConstraint(stock_quantity >= 0, name='check_stock_non_negative'),
    )

class Purchase(Base):
    __tablename__ = 'purchase'
    
    purchase_id = Column(String(30), primary_key=True)
    part_id = Column(String(20), ForeignKey('part.part_id'), nullable=False)
    supplier_id = Column(String(20), ForeignKey('supplier.supplier_id'), nullable=False)
    warehouse_id = Column(String(20), ForeignKey('warehouse.warehouse_id'), nullable=False)
    purchase_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    actual_price = Column(DECIMAL(10, 2), nullable=False)
    
    # 表级约束：确保采购业务逻辑的合理性
    # - 采购数量必须为正数（不能为零或负数）
    # - 实际采购价格必须为正数（不能为零或负数）
    __table_args__ = (
        CheckConstraint(quantity > 0, name='check_quantity_positive'),
        CheckConstraint(actual_price > 0, name='check_price_positive'),
    )