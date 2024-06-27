from rest_framework import serializers


def check_user_data(data):
    role_data = (data.get('doctor', None),
                 data.get('manager', None),
                 data.get('patient', None))

    if not any(i for i in role_data) or sum(bool(i) for i in role_data) != 1:
        raise serializers.ValidationError('Должны присутствовать подробные данные одного пользователя')



