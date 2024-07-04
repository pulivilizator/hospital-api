from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Doctor, Service, Direction


class DoctorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'name', 'surname', 'patronymic', 'birthday', 'email', 'phone']


class DoctorSerializer(serializers.ModelSerializer):
    user = DoctorUserSerializer()
    direction = serializers.CharField(source='direction.slug')

    class Meta:
        model = Doctor
        fields = '__all__'


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ['id', 'name', 'description', 'slug']


class ServiceSerializer(serializers.ModelSerializer):
    direction = serializers.CharField(source='direction.name')
    direction_slug = serializers.CharField(source='direction.slug')

    class Meta:
        model = Service
        fields = ['id', 'direction', 'name', 'description', 'price', 'slug', 'direction_slug']


class DirectionDetailSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Direction
        fields = ['id', 'name', 'description', 'slug', 'doctors', 'services']


class SpecialtySerializer(serializers.Serializer):
    specialty = serializers.CharField(max_length=255)
