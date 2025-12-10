# create_tables.py
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from models import Base
from database import test_connection
from dotenv import load_dotenv
import os

load_dotenv()

# 从环境变量获取 Supabase 数据库连接字符串
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("错误: DATABASE_URL 环境变量未设置!")

print(f"连接数据库: {DATABASE_URL.split('@')[1]}")  # 只显示主机部分

# 创建数据库引擎，专门为 Supabase 配置
engine = create_engine(DATABASE_URL)

# 首先测试连接
print("测试数据库连接...")
if test_connection():
    print("数据库连接成功!")

    # 创建所有表
    print("\n创建数据库表...")
    Base.metadata.create_all(engine)

    # 验证表是否创建成功
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result]
        print(f"成功创建 {len(tables)} 个表:")
        for table in tables:
            print(f"   - {table}")
else:
    print("数据库连接失败!")