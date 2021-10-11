from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from django.urls import reverse

from cities.models import City
from flights.models import Flight


class Route(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='название маршрута',
    )
    duration = models.DurationField(
        verbose_name='время в пути',
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
        related_name='departing_routes',
        related_query_name='departing_route',
    )
    destination = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        verbose_name='город назначения',
        related_name='arriving_routes',
        related_query_name='arriving_route',
    )
    flights = models.ManyToManyField(
        Flight,
        verbose_name='рейсы'
    )

    class Meta:
        verbose_name = 'маршрут'
        verbose_name_plural = 'маршруты'

        constraints = (
            models.UniqueConstraint(
                fields=('origin', 'destination', 'duration', 'price'),
                name='route_origin_destination_duration_price_unique',
            ),
            models.CheckConstraint(
                check=~Q(origin=F('destination')),
                name='route_origin_ne_destination',
            ),
        )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.origin}-{self.destination}"

    def get_absolute_url(self):
        return reverse('routes:route', kwargs={'pk': self.pk})
