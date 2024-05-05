import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from dishka import make_async_container, AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from sqlalchemy.ext.asyncio import AsyncEngine

from user_service.main.providers import (
    PasswordManagerProvider,
    DatabaseProvider,
    ConnectionsProvider,
    UseCasesProvider,
)
from user_service.main.web import create_app
from user_service.infrastructure.sqla_db.models import metadata_obj


@pytest_asyncio.fixture
async def container():
    container = make_async_container(
        ConnectionsProvider(db_uri='sqlite+aiosqlite:///test.db'),
        DatabaseProvider(),
        PasswordManagerProvider(),
        UseCasesProvider(),
    )
    yield container
    await container.close()


@pytest_asyncio.fixture(autouse=True)
async def prepare_db(container: AsyncContainer):
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)
        await conn.run_sync(metadata_obj.create_all)


@pytest_asyncio.fixture
async def client(container: AsyncContainer):
    app = create_app()
    setup_dishka(container, app)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test',
    ) as client:
        yield client
