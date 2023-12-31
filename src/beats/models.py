from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Table

from src.auth.models import users
from src.database import metadata

beats = Table(
    "beats",
    metadata,
    Column("beat_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.user_id)),
    Column("title", String, nullable=False),
    Column("price", String, nullable=False),
    Column("bpm", Integer, nullable=False),
    Column("image", String, nullable=False),
    Column("audio_file", String, nullable=False),
    Column("added_at", TIMESTAMP, default=datetime.utcnow),
    Column("likes_count", Integer, nullable=False),
    Column("plays_count", Integer, nullable=False),
)
