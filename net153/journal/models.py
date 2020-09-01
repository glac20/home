from django.db import models
from django.urls import reverse
from datetime import date


class Entry(models.Model):
    date = models.DateField('Entry date', default=date.today, unique=True)
    body = models.TextField('Body')

    def get_absolute_url(self):
        return reverse('journal:detail', kwargs={'date': self.date})

    def __str__(self):
        return f'{self.id},{self.date},{self.body}'
