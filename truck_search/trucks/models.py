import random

from django.core.validators import (
    MaxValueValidator, MinValueValidator, RegexValidator
)
from django.db import models


class Cargo(models.Model):
    pick_up = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        related_name='pick_up',
        to_field='zip'
    )
    delivery = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        related_name='delivery',
        to_field='zip'
    )
    weight = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )
    description = models.CharField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.description[:30]


class Truck(models.Model):
    number = models.CharField(
        max_length=5,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[0-9]{4}[A-Z]$',
                message=('Unique number must be in the format XXXXY, where X '
                         'are digits from 1000 to 9999, Y is a capital letter')
            )
        ]
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='location',
        to_field='zip'
    )
    max_weight = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        if not self.location:
            available_locations = Location.objects.all()
            random_location = random.choice(available_locations)
            self.location = random_location
        super(Truck, self).save(*args, **kwargs)


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(
        max_length=5,
        unique=True,
        validators=[
            RegexValidator(
                r'^[0-9]{5}$',
                message='Zip code is a 5-digit number.'
            )
        ]
    )
    latitude = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.city}, {self.state}'
