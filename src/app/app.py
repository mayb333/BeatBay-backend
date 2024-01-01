from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserCreate, UserRead
from src.beats.router import router as router_beats
from src.users.router import router as router_users

# logger.add("logs/app_logs.log", format="{time} {level} {message}", level="INFO")
logger.info("Started the app")


app = FastAPI()


# Allow requests from the local origin (e.g., http://localhost:5500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# app.mount("/backend/images", StaticFiles(directory="backend/images"), name="images")
# app.mount("/backend/beats_src", StaticFiles(directory="backend/beats_src"), name="beats_src")
# app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


app.include_router(router_beats)
app.include_router(router_users)
