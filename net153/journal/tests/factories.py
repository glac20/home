import factory
import factory.fuzzy
from datetime import date

from ..models import Entry


class EntryFactory(factory.django.DjangoModelFactory):

    date = factory.fuzzy.FuzzyDate(date(2008, 1, 1))
    body = factory.Faker(
        'paragraph',
        nb_sentences=3,
        variable_nb_sentences=True)

    class Meta:
        model = Entry
