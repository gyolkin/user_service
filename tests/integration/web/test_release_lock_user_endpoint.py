from uuid import UUID

import pytest
from httpx import AsyncClient
from dishka import AsyncContainer

from user_service.application.protocols.gateways import UserGateway
from user_service.application.protocols.uow import UnitOfWork
from user_service.application.models import User


@pytest.mark.asyncio
async def test_release_lock_user(
    client: AsyncClient,
    container: AsyncContainer,
):
    fake_user_id = '5b77bdba-de7b-4fcb-838f-8111b68e18ae'
    response = await client.post(f'users/{fake_user_id}/lock')
    assert response.status_code == 404

    user = User(
        login='test',
        password='password',
        project_id=UUID('5b77bdba-de7b-4fcb-838f-8111b68e18ae'),
        env='prod',
        domain='canary',
        locktime=100,
    )
    async with container() as request_container:
        user_gateway: UserGateway = await request_container.get(UserGateway)
        uow: UnitOfWork = await request_container.get(UnitOfWork)
        await user_gateway.create_user(user)
        await uow.commit()

    response = await client.post(f'users/{user.id}/release')
    assert response.status_code == 204

    async with container() as request_container:
        user_gateway: UserGateway = await request_container.get(UserGateway)
        user = await user_gateway.get_user_by_id(user.id)

    assert user is not None
    assert user.locktime == 0
