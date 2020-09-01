import pytest

from django.urls import reverse, resolve

pytestmark = pytest.mark.django_db


def test_list_reverse():
    assert reverse('blog:list') == '/blog/'


def test_list_resolve():
    assert resolve('/blog/').view_name == 'blog:list'


def test_add_reverse():
    assert reverse('blog:add') == '/blog/add/'


def test_add_resolve():
    assert resolve('/blog/add/').view_name == 'blog:add'


def test_detail_reverse(post):
    url = reverse('blog:detail', kwargs={'slug': post.slug})
    assert url == f'/blog/{post.slug}/'


def test_detail_resolve(post):
    url = f'/blog/{post.slug}/'
    assert resolve(url).view_name == 'blog:detail'
