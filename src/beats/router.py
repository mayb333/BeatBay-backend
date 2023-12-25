from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import users
from src.beats.models import beats
from src.beats.schemas import TrackCard
from src.database.database import get_async_session

router = APIRouter(prefix="/beat", tags=["Beat"])


@router.get("/trending", response_model=List[TrackCard])
async def get_popular_tracks(
    limit: int = 6, session: AsyncSession = Depends(get_async_session)
) -> List[TrackCard]:
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
            .order_by(beats.c.likes_count.desc())
            .limit(limit)
        )

        result = await session.execute(query)
        trending_tracks = result.mappings().fetchall()

        if not trending_tracks:
            raise HTTPException(
                status_code=404, detail="User not found or no tracks available"
            )
        return trending_tracks
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving tracks.",
        )
