from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.application.models import User, UserId
from user_service.application.protocols.gateways import UserGateway


class SqlaUserGateway(UserGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self) -> Sequence[User]:
        query = sa.select(User)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_user_by_id(self, user_id: UserId) -> User | None:
        return await self.session.get(User, user_id)

    async def create_user(self, user: User) -> None:
        self.session.add(user)

    async def update_user(self, user: User) -> None:
        self.session.add(user)
