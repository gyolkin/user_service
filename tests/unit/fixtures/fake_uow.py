from user_service.application.protocols.uow import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.committed = False
        self.flushed = False

    async def commit(self):
        self.committed = True

    async def flush(self):
        self.flushed = True
