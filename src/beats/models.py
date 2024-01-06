from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Beat(Base):
    __tablename__ = "beat"

    beat_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    bpm = Column(Integer, nullable=False)
    mood = Column(String, nullable=True)  # 'happy,sad,energetic'
    genre = Column(String, nullable=True)  # 'hip-hop,rock'
    tags = Column(String, nullable=True)  # 'chill,happy,sad'
    image = Column(String, nullable=True)
    audio_file = Column(String, nullable=False)
    added_at = Column(TIMESTAMP, default=datetime.utcnow)
    likes_count = Column(Integer, nullable=False, default=0)
    plays_count = Column(Integer, nullable=False, default=0)

    user = relationship("User", back_populates="beats")
    options = relationship("PurchaseOption", back_populates="beat")
    likes = relationship("Like", back_populates="beat")
    plays = relationship("BeatPlay", backref="beat")


class PurchaseOption(Base):
    __tablename__ = "purchase_option"

    option_id = Column(Integer, primary_key=True)
    beat_id = Column(Integer, ForeignKey("beat.beat_id"))
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    formats = Column(String, nullable=False)  # 'mp3,wav,stems'

    beat = relationship("Beat", back_populates="options")
