from django.contrib import admin

from apps.doctors.models import Doctor, Service


# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass