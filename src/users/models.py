from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database import Base


class Like(Base):
    __tablename__ = "like"

    like_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    beat_id = Column(Integer, ForeignKey("beat.beat_id"), primary_key=True)
    added_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", backref="likes")
    beat = relationship("Beat", backref="likes")


class Cart(Base):
    __tablename__ = "cart"

    item_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    beat_id = Column(Integer, ForeignKey("beat.beat_id"), primary_key=True)
    added_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", backref="cart")


class BeatPlay(Base):
    __tablename__ = "beat_play"

    play_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    beat_id = Column(Integer, ForeignKey("beat.beat_id"))
    played_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", backref="plays")
    beat = relationship("Beat", backref="plays")
