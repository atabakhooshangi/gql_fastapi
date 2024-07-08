import contextlib
from asyncio import current_task
from typing import AsyncIterator
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine, async_scoped_session)

from config import settings


async def get_db():
    async with sessionmanager.session() as session:
        yield session


class DatabaseSessionManager:
    def __init__(self, host: str):
        self._engine = create_async_engine(
            host,
            future=True,
            poolclass=NullPool,
            pool_pre_ping=True

        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:

        async_session = async_sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession, future=True
        )
        session = async_scoped_session(async_session, scopefunc=current_task)
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# postgresql+asyncpg://test-user:password@test-postgres:5432/test_db
sessionmanager = DatabaseSessionManager(settings.get_async_connection_url())


async def get_db_session():
    print(sessionmanager)
    async with sessionmanager.session() as session:
        yield session
