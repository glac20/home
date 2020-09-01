from django import template
from taggit.models import Tag
from django.db.models import Count

register = template.Library()


@register.simple_tag
def cloud_tags(**kwargs):
    c = kwargs.get('category')
    min_count = kwargs.get('min_count', 2)
    max_size = 150
    min_size = 20

    tags = Tag.objects.filter(
        post__category__exact=c).annotate(
        tag_count=Count('post__category')).filter(
            tag_count__gte=min_count).order_by('name').all()
    max_count = max(map(lambda x: x.tag_count, tags), default=0)
    diff = max_count - min_count
    for t in tags:
        if diff > 0:
            tag_percent = min_size + \
                (((max_size - min_size) / diff) * (t.tag_count - min_count + 1))
            color = color_calc(t.tag_count, min_count, max_count)
            t.font_size = tag_percent
            t.font_color = color

    return tags


def color_calc(tag_count, min_count, max_count):
    start_color = 'ffb448'
    end_color = '991100'

    diff = max_count - min_count

    result = []

    for i in range(3):
        s = get_dec(start_color, i * 2)
        e = get_dec(end_color, i * 2)
        diff_se = abs(s - e)

        rogob = (diff_se / diff) * (tag_count - min_count)
        if s < e:
            rogob = s + rogob
        else:
            rogob = s - rogob

        result.append('{:02X}'.format(int(rogob)))

    return ''.join(result)


def get_dec(color, offset):
    return int(color[offset:offset + 2], 16)
