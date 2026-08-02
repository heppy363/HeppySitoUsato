from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory

from app.database import Base, configure_alembic_database_url, database_metadata


def test_database_base_exposes_shared_empty_metadata() -> None:
    assert Base.metadata is database_metadata
    assert database_metadata.tables == {}
    assert database_metadata.naming_convention["pk"] == "pk_%(table_name)s"
    assert database_metadata.naming_convention["fk"] == (
        "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
    )


def test_configure_alembic_database_url_reads_backend_settings(monkeypatch) -> None:
    class StubSettings:
        database_url = "postgresql+asyncpg://stub:secret@localhost:5432/heppysitousato"

    monkeypatch.setattr("app.database.migrations.get_settings", lambda: StubSettings())
    config = Config()

    configured_url = configure_alembic_database_url(config)

    assert configured_url == StubSettings.database_url
    assert config.get_main_option("sqlalchemy.url") == StubSettings.database_url


def test_alembic_script_directory_is_registered() -> None:
    config = Config(str(Path("alembic.ini")))

    script_directory = ScriptDirectory.from_config(config)

    assert Path(script_directory.dir).resolve() == Path("migrations").resolve()
