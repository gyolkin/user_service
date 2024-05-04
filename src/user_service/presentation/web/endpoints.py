from fastapi import APIRouter, responses

from .routes.user_routes import user_router

root_router = APIRouter()
root_router.include_router(user_router)


@root_router.get('/', include_in_schema=False)
def index() -> responses.RedirectResponse:
    return responses.RedirectResponse('/docs')
