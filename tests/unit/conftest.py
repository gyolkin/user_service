import pytest

from .fakes import FakeUserGateway, FakeUnitOfWork, FakePasswordManager


@pytest.fixture
def fake_uow():
    return FakeUnitOfWork()


@pytest.fixture
def fake_gateway():
    return FakeUserGateway()


@pytest.fixture
def fake_password_manager():
    return FakePasswordManager()
