from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
    create_async_engine,
)

from user_service.infrastructure.sqla_db.models import metadata_obj  # noqa


class ConnectionsProvider(Provider):
    def __init__(self, db_uri: str, db_echo: bool):
        super().__init__()
        self.db_uri = db_uri
        self.db_echo = db_echo

    @provide(scope=Scope.APP)
    def engine(self) -> AsyncEngine:
        return create_async_engine(self.db_uri, echo=self.db_echo)

    @provide(scope=Scope.APP)
    def sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
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
