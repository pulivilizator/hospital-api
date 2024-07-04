from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import Index
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField, PhoneNumber

from .manager import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = PhoneNumberField(region='RU', unique=True, max_length=13, verbose_name='Номер телефона')
    name = models.CharField(max_length=255, verbose_name='Имя')
    surname = models.CharField(max_length=255, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=255, verbose_name='Отчество', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name', 'surname']

    objects = UserManager()

    def __str__(self):
        return self.full_name()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def full_name(self):
        if self.patronymic:
            return f'{self.surname} {self.name} {self.patronymic}'
        return f'{self.surname} {self.name}'

    def save(self, *args, **kwargs):
        if str(self.phone)[0] == '8':
            self.phone = f'+7{self.phone[1:]}'
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = (
            Index(fields=('email',)),
        )

