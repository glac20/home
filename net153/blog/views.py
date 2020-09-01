from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import redirect


from .models import Post, Comment
from .forms import CommentForm


class CategoryMixin():
    category = 'GE'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'post' in context:
            self.category = context['post'].category
        return context


class PostListView(ListView):
    model = Post
    ordering = '-created'
    paginate_by = 40
    category = 'GE'

    def get_queryset(self):
        qs = super().get_queryset()
        tags = self.request.GET.get('-tags')
        if tags:
            tags = tags.split(',')
            qs = qs.filter(tags__slug__exact=tags[0])

        qs = qs.annotate(comment_count=models.Count('comments'))
        qs = qs.prefetch_related('tags').prefetch_related(
            'related_posts').filter(category__exact=self.category)
        return qs


class PostDetailView(CategoryMixin, DetailView):
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related(
            models.Prefetch(
                'comments',
                queryset=Comment.objects.order_by('created')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostCreateView(CategoryMixin, LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body', 'category', 'tags']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class PostUpdateView(CategoryMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'body', 'category', 'tags']
    action = 'Update'


class CommentCreateView(CategoryMixin, CreateView):
    template_name = 'blog/post_detail.html'
    model = Comment
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        return redirect('blog:detail', kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(
            Post, slug=self.kwargs.get(self.slug_url_kwarg))
        self.category = context['post'].category
        context['has_previewed'] = True
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ip = self.request.META['REMOTE_ADDR']
        self.object.agent = self.request.META.get('HTTP_USER_AGENT', '')
        self.object.post = Post.objects.get(
            slug=self.kwargs.get(self.slug_url_kwarg))
        self.object.save()
        return super().form_valid(form)
