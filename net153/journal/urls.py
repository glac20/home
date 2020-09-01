from django.urls import path
from . import views

app_name = "journal"

urlpatterns = [
    path(
        route='',
        view=views.EntryListView.as_view(),
        name='list'),
    path(
        route='add/',
        view=views.EntryCreateView.as_view(),
        name='add'),
    path(
        route='<slug:date>/',
        view=views.EntryDetailView.as_view(),
        name='detail'),
    path(
        route='<slug:date>/update/',
        view=views.EntryUpdateView.as_view(),
        name='update')
]
