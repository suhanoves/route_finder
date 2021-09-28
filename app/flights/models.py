from django.db import models
from django.urls import reverse

from cities.models import City


class Flight(models.Model):
    number = models.CharField(
        verbose_name='номер рейса',
        max_length=10,
        unique=True,
    )
    duration = models.DurationField(
        verbose_name='длительность',
    )
    price = models.DecimalField(
        verbose_name='стоимость',
        max_digits=14,
        decimal_places=2,
    )
    origin = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        verbose_name='город отправления',
        related_name='departing_flights',
        related_query_name='departing_flight',
    )
    destination = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        verbose_name='город назначения',
        related_name='arriving_flights',
        related_query_name='arriving_flight',
    )

    class Meta:
        verbose_name = 'рейс'
        verbose_name_plural = 'рейсы'

    def __str__(self):
        return f"{self.origin}-{self.destination}"

    def get_absolute_url(self):
        return reverse('flights:flight', kwargs={'pk': self.pk})
