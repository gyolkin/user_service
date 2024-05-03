from abc import ABC, abstractmethod
from typing import Sequence

from user_service.application.models import User, UserId


class UserGateway(ABC):
    @abstractmethod
    async def get_users(self) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user: User) -> None:
        raise NotImplementedError
