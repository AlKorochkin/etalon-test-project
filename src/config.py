from distutils.util import strtobool
import logging
from os import getenv
from pathlib import Path

from dotenv import load_dotenv


current_dir = Path(__file__).parent
env_loaded = load_dotenv(current_dir.parents[1].joinpath(".env"))


# POSTGRES Settings
class Settings:
    POSTGRES_USER: str = getenv("POSTGRES_USER", default="test_user")
    POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", default="pg_password")
    POSTGRES_SERVER: str = getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = getenv("POSTGRES_DB", "pgdb")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    IS_VERIFIED: bool = strtobool(getenv("IS_VERIFIED", default="true"))  # type: ignore
    ACCESS_LIFETIME_SECONDS: int = int(getenv("ACCESS_LIFETIME_SECONDS", default=3600))
    ENV_MODE: str = getenv("ENV_MODE", default="prod")
    LOG_LEVEL: str = getenv("LOG_LEVEL", default="WARNING")
    SECRET: str = getenv("SECRET", default="strong_secret")
    # Redis
    REDIS_SERVER: str = getenv("REDIS_SERVER", default="redis_container")
    # Chirpstack Integration
    CHIRPSTACK_API_BASEURL: str = getenv(
        "CHIRPSTACK_API_BASEURL", default="localhost"
    )  # api base url
    CHIRPSTACK_API_KEY: str = getenv(
        "CHIRPSTACK_API_KEY", default="32b38508-8b49-4845-90ca-4dbeefce9999"
    )  # global api key
    DEFAULT_APPLICATION_ID: str = getenv(
        "DEFAULT_APPLICATION_ID", "32b38508-8b49-4845-90ca-4dbeefce9999"
    )  # default application id for existing projects, which will be created before auto-integration
    TENANT_ID: str = getenv(
        "TENANT_ID", default="32b38508-8b49-4845-90ca-4dbeefce9999"
    )  # environment tenant id(uuid for Chirpstack Tenant)


settings = Settings()

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=settings.LOG_LEVEL, format=log_format)
