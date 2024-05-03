from datetime import datetime
from uuid import UUID

from pydantic import TypeAdapter

from user_service.application.models.user import User, UserId

from .base import BaseDto


class UserCreateDto(BaseDto):
    login: str
    password: str
    project_id: UUID
    env: str
    domain: str


class UserReadDto(BaseDto):
    id: UserId
    login: str
    project_id: UUID
    env: str
    domain: str
    locktime: int
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: User) -> 'UserReadDto':
        return cls(
            id=entity.id,
            login=entity.login,
            project_id=entity.project_id,
            env=entity.env,
            domain=entity.domain,
            locktime=entity.locktime,
            created_at=entity.created_at,
        )


user_list_adapter = TypeAdapter(list[UserReadDto])
