from fastapi import APIRouter

from .routes.user import user_router

root_router = APIRouter(prefix='/api')
root_router.include_router(user_router)
