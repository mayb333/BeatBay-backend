from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Role(Base):
    __tablename__ = "role"

    role_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)

    user = relationship("User", back_populates="role")


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column("user_id", Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    profile_photo = Column(String)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey("role.role_id"))
    total_likes = Column(Integer)
    total_plays = Column(Integer)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    role = relationship("Role", back_populates="user")
    beats = relationship("Beat", back_populates="user")
    cart = relationship("Cart", back_populates="user")
    likes = relationship("Like", back_populates="user")
    plays = relationship("BeatPlay", back_populates="user")
