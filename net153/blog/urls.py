from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = "blog"

urlpatterns = [
    path(
        route='',
        view=cache_page(60 * 30)(views.PostListView.as_view()),
        name='list'),
    path(
        route='tech/',
        view=cache_page(60 * 60)(views.PostListView.as_view(category='TE')),
        name='tech-list'),
    path(
        route='add/',
        view=views.PostCreateView.as_view(),
        name='add'),
    path(
        route='<slug:slug>/',
        view=views.PostDetailView.as_view(),
        name='detail'),
    path(
        route='<slug:slug>/update/',
        view=views.PostUpdateView.as_view(),
        name='update'),
    path(
        route='comment/<slug:slug>/add/',
        view=views.CommentCreateView.as_view(),
        name='comment-add'),

]
