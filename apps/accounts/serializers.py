from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.validators import UniqueValidator

from .utils import check_user_data
from apps.doctors.models import Doctor
from apps.managers.models import Manager
from apps.patients.models import Patient


class PatientSerializer(serializers.Serializer):
    role = serializers.RegexField(regex='patient')


class DoctorSerializer(serializers.Serializer):
    role = serializers.RegexField(regex='doctor')
    specialty = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False)
    image = serializers.URLField(required=False)


class ManagerSerializer(serializers.Serializer):
    role = serializers.RegexField(regex='manager')
    description = serializers.CharField(required=False)
    image = serializers.URLField(required=False)


class UserSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(required=False)
    manager = ManagerSerializer(required=False)
    patient = PatientSerializer(required=False)

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=get_user_model().objects.all(), message='Email уже зарегистрирован')])
    phone = PhoneNumberField(region='RU', validators=[
        UniqueValidator(queryset=get_user_model().objects.all(), message='Номер телефона уже зарегистрирован')])
    name = serializers.CharField(max_length=255)
    surname = serializers.CharField(max_length=255)
    patronymic = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    birthday = serializers.DateField(required=False)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'phone', 'name', 'surname', 'patronymic', 'birthday', 'password', 'doctor', 'patient',
            'manager')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        try:
            validate_password(value)
            return value
        except DjangoValidationError as e:
            raise serializers.ValidationError(
                'Пароль должен состоять минимум из 8ми символов и содержать цифры, заглавные и строчные буквы')

    def validate(self, attrs):
        check_user_data(attrs)
        return attrs

    def create(self, validated_data):
        doctor_data = validated_data.pop('doctor', None)
        patient_data = validated_data.pop('patient', None)
        manager_data = validated_data.pop('manager', None)

        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            phone=validated_data['phone'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            patronymic=validated_data.get('patronymic', None),
            birthday=validated_data.get('birthday', None),
            password=validated_data['password'],
        )

        self.create_related_object(Doctor, user, doctor_data)
        self.create_related_object(Manager, user, manager_data)
        self.create_related_object(Patient, user, patient_data)

        return user

    @staticmethod
    def create_related_object(model, user, data: dict):
        if data:
            del data['role']
            model.objects.create(user=user, **data)
