import time
from functools import lru_cache
import re
import logging
import markdown
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from tlru_cache import tlru_cache
from net153.blog.models import AutoLink


logger = logging.getLogger(__name__)
register = template.Library()


def colorlinks(text):
    def _colorlinks(m):
        c = ''
        if re.search(r'class=', m[1], flags=re.I):
            return m[0]

        if re.search(r'\.wiki|\.edu', m[1], flags=re.I):
            c = 'class="blue"'
        elif re.search(r'net153\.net|See more', m[1], flags=re.I):
            c = ''
        elif re.search(r'github', m[1], flags=re.I):
            c = 'class="purple"'
        else:
            c = 'class="green"'
        return f'<a {c} {m[1]}>'

    return re.sub(r'<a(.*?)>', _colorlinks, text, flags=re.I)


def autolinks(text):
    auto_links = _get_auto_links
    if auto_links.cache_info().hits > 10000:
        logger.info('Clearing autolink cache')
        auto_links.cache_clear()

    for al in auto_links():

        url = escape(al['url'])
        text = re.sub(
            rf'(?<=\s)({al["name"]})(?=([\s\,\!\;]|\.\s|\:\s|[\(\)]\s))',
            rf'<a href="{url}" title="\1">\1</a>',
            text, flags=re.I)
    return text


def seemore(text):
    return text.replace('<more>', '')


def noseemore(text, post):
    s, *ss = text.split('<more>', 1)
    if len(ss):
        url = post.get_absolute_url()
        s += f'\n\n[See More...]({url} "See more: {post.slug}")'
    return s


@lru_cache(maxsize=1, typed=False)
def _get_auto_links():
    return AutoLink.objects.all().values('name', 'url')


@register.tag
def blog_print(parser, token):
    tag_name, post, *args = token.split_contents()

    return BlogPrint(post, args)


class BlogPrint(template.Node):
    # 'blog_print' is a kludge of various bloxsom plugins

    def __init__(self, post, args):
        self.post = template.Variable(post)
        self.args = ','.join(args)

    def render(self, context):
        post = self.post.resolve(context)
        text = post.body

        # remove <more> tag
        if 'seemore' in self.args:
            text = seemore(text)
        else:
            text = noseemore(text, post)

        text = markdown.markdown(text)

        # auto create keyword links
        text = autolinks(text)

        # add color class to links
        text = colorlinks(text)

        return mark_safe(text)


@register.tag
def render_time(parser, token):
    return RenderTimeNode()


class RenderTimeNode(template.Node):
    def time_diff(self):
        return '{:.4f}'.format(time.time() - self.start_t)

    def render(self, context):
        self.start_t = time.time()
        context['total_render_time'] = self.time_diff
        return ''
