from dishka import Provider, Scope, provide, alias
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.infrastructure.sqla_db.gateways import SqlaUserGateway
from user_service.application.protocols.gateways import UserGateway
from user_service.application.protocols.uow import UnitOfWork


class DatabaseProvider(Provider):
    scope = Scope.REQUEST

    user_gateway = provide(SqlaUserGateway, provides=UserGateway)
    uow = alias(source=AsyncSession, provides=UnitOfWork)
