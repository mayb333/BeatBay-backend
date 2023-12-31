from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Table

from src.auth.models import users
from src.beats.models import beats
from src.database import metadata

likes = Table(
    "likes",
    metadata,
    Column("user_id", Integer, ForeignKey(users.c.user_id)),
    Column("beat_id", Integer, ForeignKey(beats.c.beat_id)),
    Column("added_at", TIMESTAMP, default=datetime.utcnow),
)


carts = Table(
    "carts",
    metadata,
    Column("user_id", Integer, ForeignKey(users.c.user_id)),
    Column("beat_id", Integer, ForeignKey(beats.c.beat_id)),
    Column("added_at", TIMESTAMP, default=datetime.utcnow),
)
