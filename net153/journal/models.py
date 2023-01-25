from random import randint
from django.db import models
from django.urls import reverse
from datetime import date


class EntryManager(models.Manager):
    def random(self):
        count = self.aggregate(count=models.Count('id'))['count']
        return self.all()[randint(0, count - 1)]


class Entry(models.Model):
    objects = EntryManager()
    date = models.DateField('Entry date', default=date.today, unique=True)
    body = models.TextField('Body')

    def get_absolute_url(self):
        return reverse('journal:detail', kwargs={'date': self.date})

    def __str__(self):
        return f'{self.id},{self.date},{self.body}'
