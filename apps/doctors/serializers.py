from rest_framework import serializers

from .models import Doctor, Service


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['user', 'specialty', 'description', 'image']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['doctor', 'name', 'description', 'price']
