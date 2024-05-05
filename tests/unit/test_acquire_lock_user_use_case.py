from uuid import UUID

import pytest

from user_service.application.use_cases.user import AcquireLockUser
from user_service.application.models import User, UserId
from user_service.application.exceptions import (
    EntityNotExistError,
    UserAlreadyLockedError,
)
from user_service.application.constants import (
    USER_DOES_NOT_EXIST,
    USER_ALREADY_LOCKED,
)
from .fakes import FakeUserGateway, FakeUnitOfWork


@pytest.mark.asyncio
async def test_acquire_lock_user(
    fake_gateway: FakeUserGateway,
    fake_uow: FakeUnitOfWork,
):
    user = User(
        login='test',
        password='password',
        project_id=UUID('5b77bdba-de7b-4fcb-838f-8111b68e18ae'),
        env='prod',
        domain='canary',
    )
    await fake_gateway.create_user(user)

    acquire_lock = AcquireLockUser(user_gateway=fake_gateway, uow=fake_uow)
    await acquire_lock(user.id)
    updated_user = await fake_gateway.get_user_by_id(user.id)

    assert updated_user
    assert isinstance(updated_user.locktime, int)
    assert updated_user.locktime != 0
    assert fake_uow.committed


@pytest.mark.asyncio
async def test_acquire_lock_already_locked_user(
    fake_gateway: FakeUserGateway,
    fake_uow: FakeUnitOfWork,
):
    user = User(
        login='test',
        password='password',
        project_id=UUID('5b77bdba-de7b-4fcb-838f-8111b68e18ae'),
        env='prod',
        domain='canary',
    )
    await fake_gateway.create_user(user)

    acquire_lock = AcquireLockUser(user_gateway=fake_gateway, uow=fake_uow)
    await acquire_lock(user.id)
    with pytest.raises(UserAlreadyLockedError) as exc:
        await acquire_lock(user.id)

    assert str(exc.value) == USER_ALREADY_LOCKED


@pytest.mark.asyncio
async def test_acquire_lock_user_not_found(
    fake_gateway: FakeUserGateway,
    fake_uow: FakeUnitOfWork,
):
    random_user_id = UserId(UUID('5b77bdba-de7b-4fcb-838f-8111b68e18ae'))

    acquire_lock = AcquireLockUser(user_gateway=fake_gateway, uow=fake_uow)
    with pytest.raises(EntityNotExistError) as exc:
        await acquire_lock(random_user_id)

    assert str(exc.value) == USER_DOES_NOT_EXIST
