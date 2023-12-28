from datetime import datetime

from pydantic import BaseModel

from src.beats.schemas import TrackCard


class UserGet(BaseModel):
    user_id: int
    email: str
    username: str
    profile_photo: str
    registered_at: datetime
    role_id: int
    total_likes: int
    total_plays: int


class TrackCardForLiked(TrackCard):
    added_to_likes_at: datetime


class TrackCardForCart(TrackCard):
    added_to_cart_at: datetime
