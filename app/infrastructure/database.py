from collections.abc import AsyncGenerator

from dishka import Scope
from orderflow_core.di import injectable
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import Config


@injectable(scope=Scope.APP)
def get_engine(config: Config) -> AsyncEngine:
    return create_async_engine(
        config.database_url,
        echo=True,
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True,
    )


@injectable(scope=Scope.APP)
def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


@injectable(scope=Scope.REQUEST)
async def get_session(sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession]:
    async with sessionmaker() as session:
        yield session
