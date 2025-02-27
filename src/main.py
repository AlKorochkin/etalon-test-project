from contextlib import asynccontextmanager
import logging
from pathlib import Path
import shutil

from fastapi import FastAPI

from config import settings
from endpoints import projects_router
from schemas import UserRead, UserUpdate, UserCreate

from auth import fastapi_users, auth_backend

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    current_dir = Path(__file__).parent
    env = current_dir.parent.joinpath(".env")
    if not env.exists():
        shutil.copy(env.parents[1].joinpath(".env"), "../.env")
    yield


app = FastAPI(title="Demo API", version="0.1.0", lifespan=lifespan)


app.include_router(
    projects_router,
    prefix="/api",
    tags=["projects"],
)
app.include_router(
    fastapi_users.get_auth_router(
        backend=auth_backend, requires_verification=settings.IS_VERIFIED
    ),
    prefix="/api",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/api",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/users",
    tags=["users"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
