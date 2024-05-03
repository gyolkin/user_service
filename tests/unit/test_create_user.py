from uuid import uuid4

import pytest

from user_service.application.dto.user import UserCreateDto
from user_service.application.use_cases.user import CreateUser
from tests.unit.fixtures import (
    FakeUserGateway,
    FakeUnitOfWork,
    FakePasswordManager,
)


@pytest.mark.asyncio
async def test_create_user(
    fake_gateway: FakeUserGateway,
    fake_uow: FakeUnitOfWork,
    fake_password_manager: FakePasswordManager,
):
    create_user = CreateUser(
        user_gateway=fake_gateway,
        uow=fake_uow,
        password_manager=fake_password_manager,
    )
    user_data = UserCreateDto(
        login='test',
        password='password',
        project_id=uuid4(),
        env='prod',
        domain='canary',
    )
    created_user = await create_user(user_data)

    assert created_user.id
    assert user_data.login == created_user.login
    assert len(fake_gateway.users) == 1
    assert fake_uow.committed
