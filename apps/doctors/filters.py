from django.db.models import QuerySet, Value, CharField
from django.db.models.functions import Concat
from django_filters import rest_framework as filters

from apps.doctors.models import Doctor, Service


class DoctorFilter(filters.FilterSet):
    specialty = filters.CharFilter(field_name='specialty', lookup_expr='icontains')
    name = filters.CharFilter(method='filter_full_name')

    class Meta:
        model = Doctor
        fields = ['specialty', 'user']

    def filter_full_name(self, queryset: QuerySet, name: str, value: str):
        return queryset.annotate(
            full_name=Concat('user__surname', Value(' '),
                             'user__name', Value(' '),
                             'user__patronymic', output_field=CharField())
        ).filter(full_name__icontains=value)


class ServiceFilter(filters.FilterSet):
    direction = filters.CharFilter(field_name='direction__name', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Service
        fields = ['direction', 'name']
