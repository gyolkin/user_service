from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from user_service.presentation.web.endpoints import root_router
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
    )
    app.include_router(root_router)

    container = make_async_container(
        ConnectionsProvider(),
        DatabaseProvider(),
        PasswordManagerProvider(),
        UseCasesProvider(),
    )
    setup_dishka(container, app)
    return app
