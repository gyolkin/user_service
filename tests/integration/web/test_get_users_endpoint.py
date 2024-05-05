import pytest
from httpx import AsyncClient
from dishka import AsyncContainer

from user_service.application.protocols.gateways import UserGateway


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient, container: AsyncContainer):
    async with container() as request_container:
        user_gateway: UserGateway = await request_container.get(UserGateway)
        users = await user_gateway.get_users()
    response = await client.get('users')

    assert response.status_code == 200
    assert len(response.json()) == len(users)
