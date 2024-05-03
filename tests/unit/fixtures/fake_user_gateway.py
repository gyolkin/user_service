from uuid import uuid4

from user_service.application.protocols.gateways import UserGateway
from user_service.application.models import User, UserId


class FakeUserGateway(UserGateway):
    def __init__(self):
        self.users = []

    async def get_users(self) -> list[User]:
        return self.users.copy()

    async def get_user_by_id(self, user_id: UserId) -> User | None:
        for user in self.users:
            if user.id == user_id:
                return user

    async def create_user(self, user: User) -> None:
        user.id = UserId(uuid4())
        self.users.append(user)

    async def update_user(self, user: User) -> None:
        for i, existing_user in enumerate(self.users):
            if existing_user.id == user.id:
                self.users[i] = user
