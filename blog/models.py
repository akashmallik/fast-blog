from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship

from .database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = Relationship("BlogModel", back_populates="author")


class BlogModel(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = Relationship("UserModel", back_populates="blogs")
