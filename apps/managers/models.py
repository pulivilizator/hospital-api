from django.contrib.auth import get_user_model
from django.db import models


class Manager(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.user)
