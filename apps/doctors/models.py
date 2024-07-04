from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Index

from apps.utils import unique_slug_generator


class Direction(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'


class Doctor(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    direction = models.ForeignKey(Direction, related_name='doctors', on_delete=models.SET_NULL, null=True, default=None)
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.specialty} - {self.user.full_name()}'

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, self.user.full_name())
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'
        indexes = (
            Index(fields=('specialty',)),
            Index(fields=('user',)),
        )


class Service(models.Model):
    direction = models.ForeignKey(Direction, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        indexes = (
            Index(fields=('name',)),
            Index(fields=('price',)),
        )
