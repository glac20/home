import pytest
from .factories import EntryFactory
from net153.users.tests.factories import UserFactory


@pytest.fixture
def entry():
    return EntryFactory()


@pytest.fixture
def user():
    return UserFactory()
