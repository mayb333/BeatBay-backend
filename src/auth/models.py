from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)

from src.database import Base, metadata

roles = Table(
    "roles",
    metadata,
    Column("role_id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)


users = Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("profile_photo", String),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(roles.c.role_id)),
    Column("total_likes", Integer),
    Column("total_plays", Integer),
    Column("hashed_password", String(length=1024), nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = Column("user_id", Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    profile_photo = Column(String)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(roles.c.role_id))
    total_likes = Column(Integer)
    total_plays = Column(Integer)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
