from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from django.urls import reverse
from dbview.models import DbView


class Post(TimeStampedModel):
    class Category(models.TextChoices):
        GENERAL = 'GE', 'General'
        TECH = 'TE', 'Technology'

    title = models.CharField('Title of Post', max_length=70)
    body = models.TextField('Body')
    category = models.CharField(
        db_index=True,
        max_length=2,
        choices=Category.choices,
        default=Category.GENERAL,
    )
    slug = AutoSlugField(
        'Post Address',
        unique=True,
        always_update=False,
        populate_from='title')

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name='creator',
        on_delete=models.CASCADE)

    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.id},{self.title},{self.body}'


class Comment(TimeStampedModel):
    name = models.CharField('Name', max_length=32)
    url = models.TextField('URL', blank=True)
    test = models.CharField('Captcha', max_length=3)
    body = models.TextField('Comment')
    ip = models.TextField('IP Address')
    agent = models.TextField('Browser Agent', blank=True)
    post = models.ForeignKey(
        'blog.Post',
        null=False,
        related_name='comments',
        related_query_name='comments',
        on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.post.slug})


class RelatedPost(DbView):
    relatedpost_id = models.IntegerField(
        primary_key=True, db_column='relatedpost_id')
    post = models.ForeignKey(
        'blog.Post',
        db_column='post_id',
        related_name='related_posts',
        on_delete=models.DO_NOTHING)

    related_title = models.TextField()
    related_slug = models.TextField()
    related_tags = models.TextField()
    related_count = models.IntegerField(db_column='related_count')

    @classmethod
    def get_view_str(cls):
        return """CREATE VIEW blog_relatedpost AS (
            SELECT ROW_NUMBER() OVER( ) as relatedpost_id, b.id as post_id, r.*
            FROM blog_post b
            LEFT JOIN LATERAL (
              SELECT
                bp.title as related_title, bp.slug as related_slug,
                STRING_AGG(tt.name,', ') as related_tags, count(*) as related_count
                FROM blog_post bp
                INNER JOIN taggit_taggeditem tti ON tti.object_id  = bp.id
                INNER JOIN taggit_tag  tt ON tt.id = tti.tag_id
                WHERE tt.id IN ( SELECT tag_id FROM taggit_taggeditem tt3 WHERE tt3.object_id = b.id ) AND bp.id != b.id AND b.category = bp.category
                GROUP BY bp.id
                HAVING count(*) > 1
                ORDER BY count(*) DESC
                LIMIT 4
            ) AS r ON TRUE
            WHERE related_title IS NOT NULL )"""


class AutoLink(models.Model):
    name = models.TextField('Name')
    url = models.TextField('Url')
