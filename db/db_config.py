from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os

# 数据库连接字符串（请根据你的数据库配置修改这里）
driver = "mysql+mysqlconnector"
username = "root"
password = "MEIlong750712!"
host = os.getenv("DB_HOST", "localhost")
port ="3306"
database_name = "shanghai_video_translation"
DATABASE_URL = driver+"://" + username + ":" + password +  "@" + host + ":" + port +"/" + database_name

# 创建数据库引擎：负责与数据库通信，执行SQL语句
#echo参数可以打印日志，方便调试
engine = create_engine(DATABASE_URL, echo=False)

# 创建基础类，表结构的底层构建方法类，和db_table的表结构结合可以生成真正的表
Base = declarative_base()
# 创建Session类，用于数据库会话：管理数据库会话，用于执行查询、插入、更新等操作
#autocommit在关闭状态下每次执行sql语句后要更改到数据库中需要db.commit
#开启后就不用了
#默认情况下commit会包含flush，所以一般只写commit就行了
#bind指定数据库引擎，用于连接数据库
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
