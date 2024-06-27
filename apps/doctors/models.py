from django.contrib.auth import get_user_model
from django.db import models


class Doctor(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.user)


class Service(models.Model):
    doctor = models.ManyToManyField(Doctor, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

