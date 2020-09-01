import re
import pytest
from pytest_django.asserts import assertContains, assertNotContains, assertRedirects
from django.urls import reverse
from .factories import PostFactory
from ..models import Post
from ..views import PostListView, PostDetailView, CommentCreateView


pytestmark = pytest.mark.django_db


def test_blog_list_view(rf):
    request = rf.get(reverse('blog:list'))
    response = PostListView.as_view()(request)
    assertContains(response, '<title>Blog</title>')


def test_blog_list_contains_2(rf):
    assert Post.objects.count() == 0
    post1 = PostFactory(category=Post.Category.GENERAL)
    post2 = PostFactory(category=Post.Category.GENERAL)
    post3 = PostFactory(category=Post.Category.TECH)
    assert Post.objects.count() == 3

    request = rf.get(reverse('blog:list'))
    response = PostListView.as_view()(request)

    assertContains(response, post1.title)
    assertContains(response, post2.title)
    assertNotContains(response, post3.title)


def test_blog_detail_view(rf, post):
    url = reverse('blog:detail', kwargs={'slug': post.slug})
    request = rf.get(url)
    response = PostDetailView.as_view()(request, slug=post.slug)
    assertContains(response, post.slug)
    assertContains(response, post.title)
    assertContains(response, post.body)


def test_blog_create_view(client, user):
    url = reverse('blog:add')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assertContains(response, '<h3>Add Post</h3>')


def test_blog_create_form_valid(client, user):
    client.force_login(user)
    title = 'Test title'
    form_data = {
        'title': title,
        'body': 'Test body',
        'category': Post.Category.GENERAL,
        'tags': 'testing,pytest',
    }
    url = reverse('blog:add')
    client.post(url, form_data)
    post = Post.objects.get(title=title)

    assert post.category == Post.Category.GENERAL
    assert post.title == title
    assert post.creator == user
    assert 'testing' in post.tags.names()
    assert 'pytest' in post.tags.names()


def test_blog_update_view(client, user, post):
    client.force_login(user)
    url = reverse('blog:update', kwargs={'slug': post.slug})
    response = client.get(url)
    assertContains(response, '<h3>Update Post</h3>')


def test_post_update(client, user, post):
    client.force_login(user)

    body = 'New Body'

    form_data = {
        'title': post.title,
        'body': body,
        'category': post.category,
        'tags': post.tags,
    }

    url = reverse('blog:update', kwargs={'slug': post.slug})

    client.post(url, form_data)

    post.refresh_from_db()

    assert post.body == body


def test_no_auth_no_post(client, user, post):
    # these pages are for authenticated users only
    url = reverse('blog:add')
    response = client.get(url)
    assert response.status_code == 302
    assert re.search(r'login', response.url)

    response = client.post(url, {})
    assert response.status_code == 302
    assert re.search(r'login', response.url)

    url = reverse('blog:update', kwargs={'slug': post.slug})
    response = client.get(url)
    assert response.status_code == 302
    assert re.search(r'login', response.url)

    response = client.post(url, {})
    assert response.status_code == 302
    assert re.search(r'login', response.url)


def test_comment_get(rf, post):
    # add comment page only excepts post requests
    request = rf.get(reverse('blog:comment-add', kwargs={'slug': post.slug}))
    expected = reverse('blog:detail', kwargs={'slug': post.slug})
    response = CommentCreateView.as_view()(request, slug=post.slug)
    assertRedirects(response, expected, fetch_redirect_response=False)


def test_comment_create(rf, post):
    url = reverse('blog:comment-add', kwargs={'slug': post.slug})
    form_data = {
        'name': 'comment name',
        'body': 'Test comment',
        'test': 'yes',
    }

    request = rf.post(url, form_data)
    response = CommentCreateView.as_view()(request, slug=post.slug)
    assertContains(response, 'Preview your comment, then hit submit')

    form_data = {
        'name': 'comment name',
        'body': 'Test comment',
        'test': 'y',
        'submit': 'Submit',
    }

    request = rf.post(url, form_data)
    response = CommentCreateView.as_view()(request, slug=post.slug)

    assertContains(response, 'Are you a human?')

    form_data = {
        'name': 'comment name',
        'body': 'Test comment',
        'test': 'yes',
        'submit': 'Submit',
    }

    request = rf.post(url, form_data)
    response = CommentCreateView.as_view()(request, slug=post.slug)
    expected = reverse('blog:detail', kwargs={'slug': post.slug})
    assertRedirects(response, expected, fetch_redirect_response=False)

    url = reverse('blog:detail', kwargs={'slug': post.slug})
    request = rf.get(url)
    response = PostDetailView.as_view()(request, slug=post.slug)
    assertContains(response, 'Test comment')
    assertContains(response, 'comment name')
