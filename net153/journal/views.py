from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Entry


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    ordering = '-date'
    paginate_by = 40


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    slug_field = 'date'
    slug_url_kwarg = 'date'


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    slug_field = 'date'
    slug_url_kwarg = 'date'
    fields = ['date', 'body']

    def get_success_url(self):
        return reverse('journal:list')


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    slug_field = 'date'
    slug_url_kwarg = 'date'
    fields = ['date', 'body']
    action = 'Update'
