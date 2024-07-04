from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.doctors import serializers
from apps.doctors.filters import DoctorFilter, ServiceFilter
from apps.doctors.models import Doctor, Service, Direction

from django_filters import rest_framework as filters


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = serializers.DoctorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DoctorFilter
    lookup_field = 'slug'

    @action(detail=False, methods=['get'], url_path='specialties')
    def get_specialties(self, request: Request):
        queryset = Doctor.objects.values('specialty').distinct()
        serializer = serializers.SpecialtySerializer(queryset, many=True)
        return Response(serializer.data)


class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = serializers.DirectionSerializer
    lookup_field = 'slug'

    @action(detail=False, methods=['get'], url_path='homepage_directions')
    def get_homepage_directions(self, request: Request):
        queryset = Direction.objects.all()[:8]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            serializer_class = serializers.DirectionDetailSerializer
            kwargs.setdefault('context', self.get_serializer_context())
            return serializer_class(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ServiceFilter
    lookup_field = 'slug'
