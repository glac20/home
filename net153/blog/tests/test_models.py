import pytest
from .factories import PostFactory

pytestmark = pytest.mark.django_db


def test__str__():
    post = PostFactory()

    assert post.__str__() == f'{post.id},{post.title},{post.body}'
    assert str(post) == f'{post.id},{post.title},{post.body}'


def test_get_absolute_url():
    post = PostFactory()
    url = post.get_absolute_url()
    assert url == f'/blog/{post.slug}/'
