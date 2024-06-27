from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Patient
        fields = ['user']

    def get_user(self, obj):
        from apps.accounts.serializers import UserSerializer
        return UserSerializer(obj.user).data
