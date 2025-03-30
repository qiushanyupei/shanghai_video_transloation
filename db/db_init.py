from contextlib import contextmanager
from db.db_config import SessionLocal
#动态初始化数据库
@contextmanager
def get_db():
    db = SessionLocal()#
    try:
        yield db
    finally:
        db.close()
