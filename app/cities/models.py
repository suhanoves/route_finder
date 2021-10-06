from django.db import models
from django.urls import reverse


class City(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cities:city', kwargs={'pk': self.pk})

    def __lt__(self, other):
        return isinstance(other, type(self)) and self.name < other.name

    def __gt__(self, other):
        return isinstance(other, type(self)) and self.name > other.name

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name

    def __hash__(self):
        return hash(self.name)
