from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database import Base


class Like(Base):
    __tablename__ = "like"

    like_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    beat_id = Column(Integer, ForeignKey("beat.beat_id"))
    added_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="likes")
    beat = relationship("Beat", back_populates="beat_likes")


class Cart(Base):
    __tablename__ = "cart"

    item_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    beat_id = Column(Integer, ForeignKey("beat.beat_id"))
    added_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="cart")


class BeatPlay(Base):
    __tablename__ = "beat_play"

    play_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    beat_id = Column(Integer, ForeignKey("beat.beat_id"))
    played_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="plays")
    beat = relationship("Beat", back_populates="beat_plays")
