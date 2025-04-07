from sqlalchemy import Column, Integer,Boolean, String, Text, LargeBinary, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from db.db_config import Base
from datetime import datetime,timedelta

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    videos = relationship("Video", back_populates="user")
    def __repr__(self):#输出时的表示方法
        return f"<User(id={self.id}, username='{self.username}')>"

class Video(Base):
    __tablename__ = 'videos'  # 表名

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键，自增
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # 外键，关联 users 表
    filename = Column(String(255), nullable=False)  # 文件名
    filepath = Column(String(255), nullable=False)  # 文件存储路径
    newfilepath = Column(String(255), nullable=False)
    srtpath = Column(String(255), nullable=False)
    fontsize = Column(String(255), default="18px")
    color = Column(String(255), default="#ffffff")
    fontfamily = Column(String(255), default="SimSun")
    bold = Column(Boolean, default=False)
    italic = Column(Boolean, default=False)
    underline = Column(Boolean, default=False)
    #datetime是python内置的
    upload_time = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=8))  # 上传时间，默认为当前时间
    is_public = Column(Boolean, default=False)  # 是否公开，默认为 False

    # 定义与 User 表的关系
    user = relationship("User", back_populates="videos")

    def __repr__(self):
        return f"<Video(id={self.id}, user_id={self.user_id},filename='{self.filename}')>"

class Collect(Base):
    __tablename__ = 'collects'

    username = Column(String(255), primary_key=True, nullable=False)
    filename = Column(String(255), primary_key=True,nullable=False)

    def __repr__(self):
        return f"<Collect(username='{self.username}', filename='{self.filename}')>"

# class Document(Base):
#     __tablename__ = 'documents'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     subject = Column(String(255), nullable=True)
#
#     # 关系映射：一个文档可以有多个文档片段
#     chunks = relationship("DocumentChunk", back_populates="document")
#
#     def __repr__(self):
#         return f"<Document(id={self.id}, subject='{self.subject}')>"
#
# class DocumentChunk(Base):
#     __tablename__ = 'document_chunks'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     document_id = Column(Integer, ForeignKey('documents.id'), nullable=True)
#     chunk_text = Column(Text, nullable=True)
#     vectorized_chunk = Column(LargeBinary, nullable=True)
#
#     # 关系映射：一个文档片段属于一个文档
#     document = relationship("Document", back_populates="chunks")
#
#     def __repr__(self):
#         return f"<DocumentChunk(id={self.id}, document_id={self.document_id})>"