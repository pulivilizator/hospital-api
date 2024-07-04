from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display = ('email', 'phone', 'name', 'surname', 'patronymic', 'birthday', 'is_active', 'is_admin', 'created_at')
    list_filter = ('birthday', 'is_active', 'is_admin', 'created_at')

    fieldsets = [
        ('User info', {
            'fields': [
                'email', 'phone', 'name', 'surname', 'patronymic', 'birthday', 'is_active'
            ],
        }),
        ('Permissions', {
            'fields': [
                'is_admin',
            ],
        }),
    ]

    add_fieldsets = [
        (None, {
            'fields': [
                'email', 'phone', 'name', 'surname', 'patronymic', 'birthday', 'password1', 'password2'
            ],
        }),
    ]

    ordering = ('email',)

    filter_horizontal = ()
