# create_tables.py
from sqlalchemy import create_engine
from models import Base
from dotenv import load_dotenv
import os

load_dotenv()

# 替换为你的 Docker PostgreSQL 地址
DATABASE_URL = os.getenv("DATABASE_URL")

# 创建数据库引擎，用于连接数据库
# create_engine 会根据 DATABASE_URL 创建对应的数据库连接池
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # 自动建表！
print("✅ 所有表已创建")