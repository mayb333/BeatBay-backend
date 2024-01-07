from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

import src.users.models
from src.auth.models import User
from src.beats.models import Beat
from src.beats.schemas import TrackCard
from src.database.database import get_async_session

router = APIRouter(prefix="/beat", tags=["Beat"])


@router.get("/trending", response_model=List[TrackCard])
async def get_popular_beats(
    limit: int = 6, session: AsyncSession = Depends(get_async_session)
) -> List[TrackCard]:
    try:
        query = (
            select(
                Beat.__table__.columns,
                User.username,
                User.total_likes.label("user_total_likes"),
                User.total_plays.label("user_total_plays"),
                User.profile_photo,
            )
            .join(User, User.id == Beat.user_id)
            .order_by(desc(Beat.likes_count))
            .limit(limit)
        )

        result = await session.execute(query)
        trending_tracks = result.mappings().fetchall()

        if not trending_tracks:
            raise HTTPException(
                status_code=404, detail="User not found or no tracks available"
            )
        return trending_tracks
    except HTTPException as http_exp:
        # This block will catch HTTPException errors
        raise http_exp
    except Exception as exp:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving tracks. {exp}",
        )


@router.get("/feed", response_model=List[TrackCard])
async def get_beats(
    page: int = 1,
    bpm: int = None,
    lowest_price: int = None,
    highest_price: int = None,
    moods: List[str] = Query(None),
    genres: List[str] = Query(None),
    tags: List[str] = Query(None),
    key: List[str] = Query(None),  # Тональность (реализовать позже)
    session: AsyncSession = Depends(get_async_session),
) -> List[TrackCard]:
    try:
        limit = page * 10
        offset = limit - 10

        query = (
            select(
                Beat.__table__.columns,
                User.username,
                User.total_likes.label("user_total_likes"),
                User.total_plays.label("user_total_plays"),
                User.profile_photo,
            )
            .join(User, User.id == Beat.user_id)
            .limit(limit)
            .offset(offset)
        )

        if bpm:
            query = query.filter(Beat.bpm == bpm)
        if lowest_price:
            query = query.filter(Beat.price >= lowest_price)
        if highest_price:
            query = query.filter(Beat.price <= highest_price)
        if moods:
            mood_filter = [Beat.mood.ilike(f"%{mood_item}%") for mood_item in moods]
            query = query.filter(or_(*mood_filter))
        if genres:
            genre_filter = [
                Beat.genre.ilike(f"%{genre_item}%") for genre_item in genres
            ]
            query = query.filter(or_(*genre_filter))
        if tags:
            tag_filter = [Beat.tags.ilike(f"%{tag_item}%") for tag_item in tags]
            query = query.filter(or_(*tag_filter))

        print(query)

        result = await session.execute(query)
        tracks = result.mappings().fetchall()

        if not tracks:
            print("404 EXCEPTION")
            # ПОФИКСИТЬ
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No tracks found"
            )
        return tracks
    except HTTPException as http_exp:
        # This block will catch HTTPException errors
        raise http_exp
    except Exception as exp:
        print(exp)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving tracks.",
        )
