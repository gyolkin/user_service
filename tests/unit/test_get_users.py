from uuid import uuid4

import pytest

from user_service.application.use_cases.user import GetUsers
from user_service.application.models import User
from tests.unit.fixtures import FakeUserGateway


@pytest.mark.asyncio
async def test_get_users(fake_gateway: FakeUserGateway):
    user = User(
        login='test',
        password='password',
        project_id=uuid4(),
        env='prod',
        domain='canary',
    )
    await fake_gateway.create_user(user)

    get_users = GetUsers(user_gateway=fake_gateway)
    users = await get_users()

    assert len(users) == 1
    assert users[0].login == 'test'
