from xmlrpc.client import Boolean
from platformdirs import user_log_dir
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey(column="users.id", ondelete="CASCADE"), nullable=False
    )

    # Sets a relationship so when we fetch a post, it will also fetch the user data by the owner id
    owner = relationship(
        "User"
    )  # name of the class of the model of the table we want to relation to


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
