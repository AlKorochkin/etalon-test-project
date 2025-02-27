import logging
import uuid

from fastapi import Depends

from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from config import settings
from db import get_user_db
from models import User

# from utils import send_email_async

SECRET = settings.SECRET

logger = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    
    async def on_after_register(self, user, request = None):
        print(f'Пользователь {user.email} зарегистрировался')


    async def on_after_request_verify(self, user, token, request = None):
        print(token)


    async def on_after_login(self, user, request = None, response = None):
        print('Вошел пользователь', user.email)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


cookie_transport = CookieTransport()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=settings.ACCESS_LIFETIME_SECONDS)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers(get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
is_superuser = fastapi_users.current_user(active=True, superuser=True)
