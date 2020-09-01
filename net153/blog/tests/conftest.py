import pytest
from .factories import PostFactory
from net153.users.tests.factories import UserFactory


@pytest.fixture
def post():
    return PostFactory()


@pytest.fixture
def user():
    return UserFactory()
