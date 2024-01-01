import re
from typing import Any, Dict, cast

import pytest
from fastapi import status
from fastapi_users.router import ErrorCode
from httpx import AsyncClient
from sqlalchemy import insert, select

from src.auth.models import roles
from tests.conftest import async_session_maker


@pytest.mark.asyncio
class TestRegister:
    async def test_add_role(self):
        async with async_session_maker() as session:
            stmt = insert(roles).values(role_id=1, name="user", permissions=None)
            await session.execute(stmt)
            await session.commit()

            query = select(roles)
            result = await session.execute(query)
            assert result.all() == [(1, "user", None)], "Роль не добавилась"

    async def test_empty_body(self, async_client: AsyncClient):
        response = await async_client.post("/auth/register", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_missing_email(self, async_client: AsyncClient):
        json = {"password": "lol_pass", "username": "lol", "role_id": 1}
        response = await async_client.post("/auth/register", json=json)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_missing_password(self, async_client: AsyncClient):
        json = {"email": "lol@gmail.com", "username": "lol", "role_id": 1}
        response = await async_client.post("/auth/register", json=json)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_missing_username(self, async_client: AsyncClient):
        json = {"email": "lol@gmail.com", "password": "lol_pass", "role_id": 1}
        response = await async_client.post("/auth/register", json=json)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_missing_role_id(self, async_client: AsyncClient):
        json = {"email": "lol@gmail.com", "password": "lol_pass", "username": "lol"}
        response = await async_client.post("/auth/register", json=json)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_wrong_email(self, async_client: AsyncClient):
        json = {"email": "lol", "password": "lol_pass", "username": "lol", "role_id": 1}
        response = await async_client.post("/auth/register", json=json)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_wrong_password(self, async_client: AsyncClient):
        json = {
            "email": "lol@gmail.com",
            "password": "a",
            "username": "lol",
            "role_id": 1,
        }
        response = await async_client.post("/auth/register", json=json)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = cast(Dict[str, Any], response.json())
        assert data["detail"] == {
            "code": ErrorCode.REGISTER_INVALID_PASSWORD,
            "reason": "Password should be at least 3 characters",
        }

    async def test_valid_body(self, async_client: AsyncClient):
        json = {
            "email": "lol.kek@gmail.com",
            "password": "lol",
            "username": "lol",
            "role_id": 1,
        }
        response = await async_client.post("/auth/register", json=json)
        assert response.status_code == status.HTTP_201_CREATED

        data = cast(Dict[str, Any], response.json())
        assert "hashed_password" not in data
        assert "password" not in data
        assert data["id"] is not None

    @pytest.mark.parametrize("email", ["lol.kek@gmail.com", "Lol.Kek@gmail.com"])
    async def test_existing_user(self, email, async_client: AsyncClient):
        json = {"email": email, "password": "lol", "username": "lol", "role_id": 1}
        response = await async_client.post("/auth/register", json=json)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data["detail"] == ErrorCode.REGISTER_USER_ALREADY_EXISTS


@pytest.mark.asyncio
class TestLogin:
    async def test_empty_body(self, async_client: AsyncClient):
        response = await async_client.post("/auth/login", data={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_missing_username(self, async_client: AsyncClient):
        data = {"password": "lol"}
        response = await async_client.post("/auth/login", data=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_missing_password(self, async_client: AsyncClient):
        data = {"username": "lol.kek@gmail.com"}
        response = await async_client.post("/auth/login", data=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_not_existing_user(self, async_client: AsyncClient):
        data = {"username": "lancelot@camelot.bt", "password": "guinevere"}
        response = await async_client.post("/auth/login", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = cast(Dict[str, Any], response.json())
        assert data["detail"] == ErrorCode.LOGIN_BAD_CREDENTIALS

    async def test_wrong_password(self, async_client: AsyncClient):
        json = {
            "email": "test_wrong_pass@gmail.com",
            "password": "lol",
            "username": "lol",
            "role_id": 1,
        }
        response = await async_client.post("/auth/register", json=json)

        data = {"username": "test_wrong_pass@gmail.com", "password": "wrong_pass"}
        response = await async_client.post("/auth/login", data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = cast(Dict[str, Any], response.json())
        assert data["detail"] == ErrorCode.LOGIN_BAD_CREDENTIALS

    async def test_valid_body(self, async_client: AsyncClient):
        json = {
            "email": "test_valid_body@gmail.com",
            "password": "lol",
            "username": "lol",
            "role_id": 1,
        }
        response = await async_client.post("/auth/register", json=json)

        data = {"username": "test_valid_body@gmail.com", "password": "lol"}
        response = await async_client.post("/auth/login", data=data)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert isinstance(response.cookies["beats"], str)

        pattern = r"^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+$"  # JWT pattern
        assert re.match(pattern, response.cookies["beats"])


@pytest.mark.asyncio
class TestLogout:
    async def test_missing_token(self, async_client: AsyncClient):
        response = await async_client.post("/auth/logout")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_wrong_token(self, async_client: AsyncClient):
        response = await async_client.post(
            "/auth/logout", cookies={"beats": "wrong_token"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_valid_logout(self, async_client: AsyncClient):
        json = {
            "email": "test_valid_logout@gmail.com",
            "password": "lol",
            "username": "lol",
            "role_id": 1,
        }
        response = await async_client.post("/auth/register", json=json)

        data = {"username": "test_valid_logout@gmail.com", "password": "lol"}
        response = await async_client.post("/auth/login", data=data)

        jwt_token = response.cookies["beats"]
        response = await async_client.post("/auth/logout", cookies={"beats": jwt_token})

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.cookies.get("beats") is None
