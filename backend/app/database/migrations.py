from alembic.config import Config
from sqlalchemy import MetaData

from app.core.config import get_settings
from app.database.base import database_metadata


def configure_alembic_database_url(config: Config) -> str:
    database_url = get_settings().database_url
    config.set_main_option("sqlalchemy.url", database_url)
    return database_url


def get_target_metadata() -> MetaData:
    return database_metadata
