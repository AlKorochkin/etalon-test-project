import asyncio
import logging
import time
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from models import User

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
ASYNC_SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
    "postgresql", "postgresql+asyncpg"
)
ECHO_POOL = False
ECHO_DB = False

if settings.ENV_MODE != "prod":
    ECHO_POOL = "debug"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=ECHO_DB,
    echo_pool=ECHO_POOL,
)
async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=ECHO_DB,
    echo_pool=ECHO_POOL,
)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger(__name__)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
