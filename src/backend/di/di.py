import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from aiohttp import ClientSession
from fastapi import FastAPI
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class SessionManager:
    sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None
    _engine: Optional[AsyncEngine] = None
    _started = False

    @classmethod
    async def setup(cls) -> None:
        if cls._started:
            return
        try:
            postgres_url = URL.create(
                os.environ["POSTGRES_DRIVER"],
                os.environ["POSTGRES_USER"],
                os.environ["POSTGRES_PASSWORD"],
                os.environ["POSTGRES_HOST"],
                int(os.environ["POSTGRES_PORT"]),
                os.environ["POSTGRES_DB"],
            )
            cls._engine = create_async_engine(
                postgres_url,
                pool_pre_ping=True,
                pool_size=20,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=1800,
            )
            cls.sessionmaker = async_sessionmaker(
                cls._engine, class_=AsyncSession, expire_on_commit=False
            )
            cls._started = True
        except Exception:
            await cls.close()
            raise

    @classmethod
    async def close(cls) -> None:
        if cls._engine is not None:
            try:
                await cls._engine.dispose()
            finally:
                cls._engine = None
                cls.sessionmaker = None
        cls._started = False

    @classmethod
    async def session_factory(cls) -> AsyncGenerator[AsyncSession, None]:
        if not cls.sessionmaker or not cls._started:
            raise RuntimeError(
                "Sessionmaker not initialized; SessionManager.setup() was not called"
            )
        async with cls.sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


class ClientSessionManager:
    client_session: Optional[ClientSession] = None
    _started = False

    @classmethod
    async def setup(cls) -> None:
        if cls._started:
            return
        try:
            cls.client_session = ClientSession()
            cls._started = True
        except Exception:
            await cls.close()
            raise

    @classmethod
    async def close(cls) -> None:
        if cls.client_session is not None:
            try:
                await cls.client_session.close()
            finally:
                cls.client_session = None
        cls._started = False

    @classmethod
    async def client_session_factory(cls) -> AsyncGenerator[ClientSession, None]:
        if not cls.client_session or not cls._started:
            raise RuntimeError(
                "ClientSession not initialized; ClientSessionManager.setup() was not called"
            )
        yield cls.client_session


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await SessionManager.setup()
    await ClientSessionManager.setup()
    yield
    await ClientSessionManager.close()
    await SessionManager.close()
