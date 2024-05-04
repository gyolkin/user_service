from dishka import Provider, Scope, provide

from user_service.application.use_cases.user import (
    GetUsers,
    CreateUser,
    AcquireLockUser,
    ReleaseLockUser,
)
from user_service.application.protocols import gateways, uow, password_manager


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_users(
        self,
        user_gateway: gateways.UserGateway,
    ) -> GetUsers:
        return GetUsers(
            user_gateway=user_gateway,
        )

    @provide
    def create_user(
        self,
        user_gateway: gateways.UserGateway,
        uow: uow.UnitOfWork,
        password_manager: password_manager.PasswordManager,
    ) -> CreateUser:
        return CreateUser(
            user_gateway=user_gateway,
            uow=uow,
            password_manager=password_manager,
        )

    @provide
    def acquire_lock_user(
        self,
        user_gateway: gateways.UserGateway,
        uow: uow.UnitOfWork,
    ) -> AcquireLockUser:
        return AcquireLockUser(
            user_gateway=user_gateway,
            uow=uow,
        )

    @provide
    def release_lock_user(
        self,
        user_gateway: gateways.UserGateway,
        uow: uow.UnitOfWork,
    ) -> ReleaseLockUser:
        return ReleaseLockUser(
            user_gateway=user_gateway,
            uow=uow,
        )
