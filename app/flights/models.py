from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q
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
        validators=[
            MinValueValidator(timedelta(minutes=1)),
        ]
    )
    price = models.DecimalField(
        verbose_name='стоимость',
        max_digits=14,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01')),
        ]
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

        constraints = (
            models.UniqueConstraint(
                fields=('origin', 'destination', 'duration', 'price'),
                name='origin_destination_duration_price_unique',
            ),
            models.CheckConstraint(
                check=~Q(origin=F('destination')),
                name='origin_ne_destination',
            ),
            models.CheckConstraint(
                check=Q(duration__gt=timedelta(minutes=1)),
                name='duration_gt_1_minute',
            ),
            models.CheckConstraint(
                check=Q(price__gt=Decimal('0')),
                name='price_gt_0',
            ),
        )

    def clean(self):
        # unique flight check
        similar_flights = Flight.objects.filter(
            origin=self.origin,
            destination=self.destination,
            duration=self.duration,
            price=self.price,
        ).exclude(
            pk=self.pk
        )

        if similar_flights.exists():
            raise ValidationError(
                'Рейс с такими характеристиками уже существует',
                code='not_unique_flight'
            )

        # origin != destination check
        if self.origin == self.destination:
            raise ValidationError(
                'Город отправления и город назначения должны отличаться',
                code='cities_equal',
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} {self.origin}-{self.destination}"

    def get_absolute_url(self):
        return reverse('flights:flight', kwargs={'pk': self.pk})
