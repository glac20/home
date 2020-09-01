import pytest

from django.urls import reverse, resolve

pytestmark = pytest.mark.django_db


def test_list_reverse():
    assert reverse('journal:list') == '/journal/'


def test_list_resolve():
    assert resolve('/journal/').view_name == 'journal:list'


def test_add_reverse():
    assert reverse('journal:add') == '/journal/add/'


def test_add_resolve():
    assert resolve('/journal/add/').view_name == 'journal:add'


def test_update_reverse(entry):
    url = reverse('journal:detail', kwargs={'date': entry.date})
    assert url == f'/journal/{entry.date}/'


def test_update_resolve(entry):
    url = f'/journal/{entry.date}/'
    assert resolve(url).view_name == 'journal:detail'


def test_detail_reverse(entry):
    url = reverse('journal:detail', kwargs={'date': entry.date})
    assert url == f'/journal/{entry.date}/'


def test_detail_resolve(entry):
    url = f'/journal/{entry.date}/'
    assert resolve(url).view_name == 'journal:detail'
