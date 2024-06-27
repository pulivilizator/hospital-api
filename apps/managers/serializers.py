from rest_framework import serializers

from .models import Manager


class ManagerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(required=False)
    description = serializers.CharField(required=False)
    image = serializers.URLField(required=False)

    class Meta:
        model = Manager
        fields = ['user', 'description', 'image']

    def get_user(self, obj):
        from apps.accounts.serializers import UserSerializer
        return UserSerializer(obj.user).data
