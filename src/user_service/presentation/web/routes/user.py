from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, inject

from user_service.application.dto.user import UserReadDto, UserCreateDto
from user_service.application.use_cases.user import (
    GetUsers,
    CreateUser,
    AcquireLockUser,
    ReleaseLockUser,
)
from user_service.application.models import UserId

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.get('')
@inject
async def get_users(
    get_users: FromDishka[GetUsers],
) -> list[UserReadDto]:
    """Returns a list of users"""
    return await get_users()


@user_router.post('', status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user_data: UserCreateDto,
    create_user: FromDishka[CreateUser],
) -> UserReadDto:
    """Creates and returns a new user"""
    return await create_user(user_data)


@user_router.post('/{user_id}/lock', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def acquire_lock_user(
    user_id: UserId,
    acquire_lock_user: FromDishka[AcquireLockUser],
) -> None:
    """Locks the user"""
    return await acquire_lock_user(user_id)


@user_router.post('/{user_id}/release', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def release_lock_user(
    user_id: UserId,
    release_lock_user: FromDishka[ReleaseLockUser],
) -> None:
    """Unlocks the user"""
    return await release_lock_user(user_id)
