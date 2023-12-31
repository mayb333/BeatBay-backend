import pytest
from sqlalchemy import insert, select

from src.auth.models import roles
from tests.conftest import async_session_maker, client


@pytest.mark.asyncio
async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(roles).values(role_id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(roles)
        result = await session.execute(query)
        assert result.all() == [(1, "admin", None)], "Роль не добавилась"


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "string",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "string",
            "role_id": 1,
        },
    )

    assert response.status_code == 201
