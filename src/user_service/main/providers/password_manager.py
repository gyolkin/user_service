from dishka import Provider, Scope, provide

from user_service.infrastructure.passlib_password_manager import (
    PasslibPasswordHasher,
)
from user_service.application.protocols.password_manager import PasswordManager


class PasswordManagerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def password_manager(self) -> PasswordManager:
        return PasslibPasswordHasher()
