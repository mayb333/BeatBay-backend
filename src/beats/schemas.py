from datetime import datetime

from pydantic import BaseModel


class TrackCard(BaseModel):
    """Class for validation cards for tracks"""

    beat_id: int
    user_id: int
    title: str
    price: str
    bpm: int
    mood: str
    genre: str
    tags: str
    image: str
    mp3_file: str
    added_at: datetime
    likes_count: int
    plays_count: int
    username: str
    user_total_likes: int
    user_total_plays: int
    profile_photo: str
