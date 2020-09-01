from django.template.defaultfilters import slugify

import factory
import factory.fuzzy

from net153.users.tests.factories import UserFactory
from ..models import Post


class PostFactory(factory.django.DjangoModelFactory):

    title = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda o: slugify(o.title))
    body = factory.Faker(
        'paragraph',
        nb_sentences=3,
        variable_nb_sentences=True)
    category = factory.fuzzy.FuzzyChoice([x[0] for x in Post.Category.choices])
    creator = factory.SubFactory(UserFactory)
    tags = factory.fuzzy.FuzzyText(chars='abcdefghij,')

    class Meta:
        model = Post
