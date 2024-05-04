import os
from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)

from user_service.infrastructure.sqla_db.models import metadata_obj  # noqa


class ConnectionsProvider(Provider):
    @provide(scope=Scope.APP)
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        engine = create_async_engine(
            os.getenv('DB_URI', 'sqlite+aiosqlite:///dev.db'),
            echo=True,
        )
        return async_sessionmaker(
            engine,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def session(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session
