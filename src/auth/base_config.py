from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from src.auth.manager import get_user_manager
from src.auth.models import User
from src.config import ACCESS_TOKEN_EXPIRE_SECONDS, SECRET_KEY

cookie_transport = CookieTransport(
    cookie_name="beats", cookie_max_age=ACCESS_TOKEN_EXPIRE_SECONDS
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=ACCESS_TOKEN_EXPIRE_SECONDS)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

get_current_user = fastapi_users.current_user()
