import pytest
from .factories import EntryFactory

pytestmark = pytest.mark.django_db


def test__str__():
    post = EntryFactory()

    assert post.__str__() == f'{post.id},{post.date},{post.body}'
    assert str(post) == f'{post.id},{post.date},{post.body}'


def test_get_absolute_url():
    post = EntryFactory()
    url = post.get_absolute_url()
    assert url == f'/journal/{post.date}/'
