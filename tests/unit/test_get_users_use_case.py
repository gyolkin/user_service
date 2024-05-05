from uuid import UUID

import pytest

from user_service.application.use_cases.user import GetUsers
from user_service.application.models import User
from .fakes import FakeUserGateway


@pytest.mark.asyncio
async def test_get_users(fake_gateway: FakeUserGateway):
    user = User(
        login='test',
        password='password',
        project_id=UUID('5b77bdba-de7b-4fcb-838f-8111b68e18ae'),
        env='prod',
        domain='canary',
    )
    await fake_gateway.create_user(user)

    get_users = GetUsers(user_gateway=fake_gateway)
    users = await get_users()

    assert len(users) == 1
    assert users[0].login == 'test'
