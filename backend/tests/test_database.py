from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.database import DatabaseSessionManager, DatabaseSettings


def build_manager(engine: AsyncEngine | None = None) -> DatabaseSessionManager:
    return DatabaseSessionManager(
        DatabaseSettings(url="postgresql+asyncpg://user:password@localhost/database"),
        engine=engine,
    )


def test_database_session_manager_configures_async_sessions() -> None:
    engine = MagicMock(spec=AsyncEngine)

    manager = build_manager(engine)
    session = manager.session_factory()

    assert isinstance(session, AsyncSession)
    assert manager.engine is engine
    assert session.sync_session.expire_on_commit is False
    assert session.sync_session.autoflush is False


@pytest.mark.asyncio
async def test_database_session_rolls_back_and_closes_on_error() -> None:
    manager = build_manager(MagicMock(spec=AsyncEngine))
    session = AsyncMock(spec=AsyncSession)
    manager.session_factory = MagicMock(return_value=session)

    with pytest.raises(RuntimeError, match="failure"):
        async with manager.session():
            raise RuntimeError("failure")

    session.rollback.assert_awaited_once_with()
    session.close.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_database_session_closes_after_success() -> None:
    manager = build_manager(MagicMock(spec=AsyncEngine))
    session = AsyncMock(spec=AsyncSession)
    manager.session_factory = MagicMock(return_value=session)

    async with manager.session() as yielded_session:
        assert yielded_session is session

    session.rollback.assert_not_awaited()
    session.close.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_database_manager_disposes_shared_engine() -> None:
    engine = MagicMock(spec=AsyncEngine)
    engine.dispose = AsyncMock()
    manager = build_manager(engine)

    await manager.dispose()

    engine.dispose.assert_awaited_once_with()
