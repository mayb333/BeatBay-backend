from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import users
from src.beats.models import beats
from src.beats.schemas import TrackCard
from src.database import get_async_session
from src.users.models import carts, likes
from src.users.schemas import TrackCardForCart, TrackCardForLiked, UserGet

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/{user_id}", response_model=UserGet)
async def get_user_profile(
    user_id: int, session: AsyncSession = Depends(get_async_session)
) -> UserGet:
    try:
        query = select(
            users.c.user_id,
            users.c.email,
            users.c.username,
            users.c.profile_photo,
            users.c.registered_at,
            users.c.role_id,
            users.c.total_likes,
            users.c.total_plays,
        ).where(users.c.user_id == user_id)

        result = await session.execute(query)
        user_info = result.mappings().first()

        if user_info is not None:
            return user_info
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving user.",
        )


@router.get("/{user_id}/tracks", response_model=List[TrackCard])
async def get_user_tracks(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = (
            select(
                beats,
                users.c.username,
                users.c.total_likes.label("user_total_likes"),
                users.c.total_plays.label("user_total_plays"),
                users.c.profile_photo,
            )
            .join(users, users.c.user_id == beats.c.user_id)
            .filter(beats.c.user_id == user_id)
        )

        result = await session.execute(query)
        user_tracks = result.mappings().fetchall()

        if not user_tracks:
            raise HTTPException(
                status_code=404, detail="User not found or no tracks available"
            )
        return user_tracks
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving tracks.",
        )


@router.get("/{user_id}/cart", response_model=List[TrackCardForCart])
async def get_user_cart(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = (
            select(
                carts.c.beat_id,
                carts.c.user_id,
                carts.c.added_at.label("added_to_cart_at"),
                beats.c.title,
                beats.c.price,
                beats.c.bpm,
                beats.c.image,
                beats.c.audio_file,
                beats.c.added_at,
                beats.c.likes_count,
                beats.c.plays_count,
                users.c.username,
                users.c.total_likes.label("user_total_likes"),
                users.c.total_plays.label("user_total_plays"),
                users.c.profile_photo,
            )
            .join(users, users.c.user_id == carts.c.user_id)
            .join(beats, beats.c.beat_id == carts.c.beat_id)
            .filter(carts.c.user_id == user_id)
        )

        result = await session.execute(query)
        user_cart_tracks = result.mappings().fetchall()

        if not user_cart_tracks:
            raise HTTPException(
                status_code=404, detail="User not found or no tracks available"
            )
        return user_cart_tracks
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving cart.",
        )


@router.get("/{user_id}/liked", response_model=List[TrackCardForLiked])
async def get_user_cart(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = (
            select(
                likes.c.beat_id,
                likes.c.user_id,
                likes.c.added_at.label("added_to_likes_at"),
                beats.c.title,
                beats.c.price,
                beats.c.bpm,
                beats.c.image,
                beats.c.audio_file,
                beats.c.added_at,
                beats.c.likes_count,
                beats.c.plays_count,
                users.c.username,
                users.c.total_likes.label("user_total_likes"),
                users.c.total_plays.label("user_total_plays"),
                users.c.profile_photo,
            )
            .join(users, users.c.user_id == likes.c.user_id)
            .join(beats, beats.c.beat_id == likes.c.beat_id)
            .filter(likes.c.user_id == user_id)
        )

        result = await session.execute(query)
        user_liked_tracks = result.mappings().fetchall()

        if not user_liked_tracks:
            raise HTTPException(
                status_code=404, detail="User not found or no tracks available"
            )
        return user_liked_tracks
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving liked tracks.",
        )
