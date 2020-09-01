import re
import pytest
from pytest_django.asserts import assertContains
from django.urls import reverse
from .factories import EntryFactory
from ..models import Entry
from ..views import EntryListView, EntryDetailView


pytestmark = pytest.mark.django_db


def test_journal_list_view(rf, user):
    request = rf.get(reverse('journal:list'))
    request.user = user
    response = EntryListView.as_view()(request)
    assertContains(response, '<title>Journal</title>')


def test_journal_list_contains_2(rf, user):
    assert Entry.objects.count() == 0
    post1 = EntryFactory()
    post2 = EntryFactory()
    post3 = EntryFactory()
    assert Entry.objects.count() == 3

    request = rf.get(reverse('journal:list'))
    request.user = user
    response = EntryListView.as_view()(request)

    assertContains(response, post1.body)
    assertContains(response, post2.body)
    assertContains(response, post3.body)


def test_journal_detail_view(rf, user, entry):
    url = reverse('journal:detail', kwargs={'date': entry.date})
    request = rf.get(url)
    request.user = user
    response = EntryDetailView.as_view()(request, date=entry.date)
    assertContains(response, entry.date)
    assertContains(response, entry.body)


def test_journal_create_view(client, user):
    url = reverse('journal:add')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assertContains(response, '<h3>New Entry</h3>')


def test_journal_create_form_valid(client, user):
    client.force_login(user)
    body = 'Test body'
    date = '2010-01-02'
    form_data = {
        'date': date,
        'body': body
    }
    url = reverse('journal:add')
    client.post(url, form_data)
    entry = Entry.objects.get(date=date)

    assert entry.body == body


def test_journal_update_view(client, user, entry):
    client.force_login(user)
    url = reverse('journal:update', kwargs={'date': entry.date})
    response = client.get(url)
    assertContains(response, '<h3>Update Entry</h3>')


def test_entry_update(client, user, entry):
    client.force_login(user)

    body = 'New Body'

    form_data = {
        'date': entry.date,
        'body': body,
    }

    url = reverse('journal:update', kwargs={'date': entry.date})

    client.post(url, form_data)

    entry.refresh_from_db()

    assert entry.body == body


def test_no_auth_no_post(client, user, entry):
    # these pages are for authenticated users only
    url = reverse('journal:list')
    response = client.get(url)
    assert response.status_code == 302
    assert re.search(r'login', response.url)

    url = reverse('journal:add')
    response = client.get(url)
    assert response.status_code == 302
    assert re.search(r'login', response.url)

    response = client.post(url, {})
    assert response.status_code == 302
    assert re.search(r'login', response.url)

    url = reverse('journal:update', kwargs={'date': entry.date})
    response = client.get(url)
    assert response.status_code == 302
    assert re.search(r'login', response.url)

    response = client.post(url, {})
    assert response.status_code == 302
    assert re.search(r'login', response.url)

    url = reverse('journal:detail', kwargs={'date': entry.date})
    response = client.get(url)
    assert response.status_code == 302
    assert re.search(r'login', response.url)
