import calendar
from datetime import datetime

from user_service.application.protocols import gateways, uow, password_manager
from user_service.application.dto.user import (
    UserReadDto,
    UserCreateDto,
    user_list_adapter,
)
from user_service.application.models import User, UserId
from user_service.application.exceptions import (
    EntityNotExistError,
    UserAlreadyLockedError,
)
from user_service.application.constants import (
    USER_DOES_NOT_EXIST,
    USER_ALREADY_LOCKED,
)


class GetUsers:
    def __init__(
        self,
        user_gateway: gateways.UserGateway,
    ):
        self.user_gateway = user_gateway

    async def __call__(self) -> list[UserReadDto]:
        users = await self.user_gateway.get_users()
        return user_list_adapter.validate_python(users)


class CreateUser:
    def __init__(
        self,
        user_gateway: gateways.UserGateway,
        uow: uow.UnitOfWork,
        password_manager: password_manager.PasswordManager,
    ):
        self.user_gateway = user_gateway
        self.uow = uow
        self.password_manager = password_manager

    async def __call__(self, user_data: UserCreateDto) -> UserReadDto:
        hashed_password = self.password_manager.hash_password(
            password=user_data.password,
        )
        user = User(
            login=user_data.login,
            password=hashed_password,
            project_id=user_data.project_id,
            env=user_data.env,
            domain=user_data.domain,
        )
        await self.user_gateway.create_user(user)
        await self.uow.commit()
        return UserReadDto.from_entity(user)


class AcquireLockUser:
    def __init__(
        self,
        user_gateway: gateways.UserGateway,
        uow: uow.UnitOfWork,
    ):
        self.user_gateway = user_gateway
        self.uow = uow

    async def __call__(self, user_id: UserId) -> None:
        user = await self.user_gateway.get_user_by_id(user_id)
        if user is None:
            raise EntityNotExistError(USER_DOES_NOT_EXIST)
        if user.locktime != 0:
            raise UserAlreadyLockedError(USER_ALREADY_LOCKED)
        user.locktime = calendar.timegm(datetime.now().timetuple())
        await self.user_gateway.update_user(user)
        await self.uow.commit()


class ReleaseLockUser:
    def __init__(
        self,
        user_gateway: gateways.UserGateway,
        uow: uow.UnitOfWork,
    ):
        self.user_gateway = user_gateway
        self.uow = uow

    async def __call__(self, user_id: UserId) -> None:
        user = await self.user_gateway.get_user_by_id(user_id)
        if user is None:
            raise EntityNotExistError(USER_DOES_NOT_EXIST)
        user.locktime = 0
        await self.user_gateway.update_user(user)
        await self.uow.commit()
