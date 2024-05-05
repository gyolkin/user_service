from uuid import UUID

import pytest
from httpx import AsyncClient
from dishka import AsyncContainer

from user_service.application.protocols.gateways import UserGateway
from user_service.application.models import UserId


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, container: AsyncContainer):
    request = {
        'login': 'test',
        'password': 'password',
        'project_id': '5b77bdba-de7b-4fcb-838f-8111b68e18ae',
        'env': 'prod',
        'domain': 'canary',
    }
    response = await client.post('users', json=request)
    assert response.status_code == 201

    json_response = response.json()
    expected = (
        'id',
        'login',
        'project_id',
        'env',
        'domain',
        'locktime',
        'created_at',
    )
    assert all(key in expected for key in json_response)

    async with container() as request_container:
        user_gateway: UserGateway = await request_container.get(UserGateway)
        user = await user_gateway.get_user_by_id(
            UserId(UUID(json_response['id'])),
        )

    assert user is not None
    assert user.login == request['login']
    assert user.password != request['password']
