import os

from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from user_service.presentation.web.endpoints import root_router
from user_service.presentation.web.exception_handlers import (
    setup_exception_handlers,
)
from user_service.main.providers import (
    PasswordManagerProvider,
    DatabaseProvider,
    ConnectionsProvider,
    UseCasesProvider,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title='Users For E2E Testing',
        version='0.1.0',
        description='Test task for VK Internship',
    )
    app.include_router(root_router)
    setup_exception_handlers(app)
    return app


def create_production_app() -> FastAPI:
    app = create_app()
    container = make_async_container(
        ConnectionsProvider(
            db_uri=os.getenv('DB_URI', 'sqlite+aiosqlite:///dev.db'),
            db_echo=bool(os.getenv('DEBUG', True)),
        ),
        DatabaseProvider(),
        PasswordManagerProvider(),
        UseCasesProvider(),
    )
    setup_dishka(container, app)
    return app
