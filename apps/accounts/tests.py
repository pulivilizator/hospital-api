from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework import test, status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from .serializers import UserSerializer
from .views import RegistrationAPIView, LoginAPIView, LogoutAPIView


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_data = {
            'email': 'testuser@example.com',
            'phone': '+79001234567',
            'name': 'Test',
            'surname': 'User',
            'patronymic': 'Patronymic',
            'birthday': '1990-01-01',
            'password': 'password123'
        }
        cls.user = get_user_model().objects.create_user(**cls.user_data)

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()
        super().tearDownClass()

    def test_create_user(self):
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.phone, self.user_data['phone'])
        self.assertEqual(self.user.name, self.user_data['name'])
        self.assertEqual(self.user.surname, self.user_data['surname'])
        self.assertEqual(self.user.patronymic, self.user_data['patronymic'])
        self.assertEqual(self.user.birthday, self.user_data['birthday'])
        self.assertTrue(self.user.check_password(self.user_data['password']))

    def test_unique_email(self):
        with self.assertRaises(Exception):
            get_user_model().objects.create_user(**self.user_data)

    def test_unique_phone(self):
        self.user_data['email'] = 'newemail@example.com'
        with self.assertRaises(Exception):
            get_user_model().objects.create_user(**self.user_data)

    def test_default_params(self):
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_admin)

    def test_str_method(self):
        self.assertEqual(str(self.user), self.user_data['email'])

    def test_is_staff_property(self):
        self.assertFalse(self.user.is_staff)
        self.user.is_admin = True
        self.assertTrue(self.user.is_staff)

    def test_has_perms(self):
        self.assertTrue(self.user.has_perm('any_perm'))
        self.assertTrue(self.user.has_module_perms('any_label'))


class UserSerializerTest(TestCase):
    def setUp(self):
        self.doctor_data = {'doctor': {
            'role': 'doctor',
            'description': 'description',
            'specialty': 'speciality'
        },
            'email': 'testuser@example.com',
            'phone': '+79001234567'}
        self.patient_data = {'patient': {'role': 'patient'},
                             'email': 'testuser@example2.com',
                             'phone': '+79001234568',
                             }
        self.manager_data = {'manager': {
            'role': 'manager',
            'description': 'description',
            'address': 'address'
        },
            'email': 'testuser@example1.com',
            'phone': '+79001234566',
        }
        self.user_data = {
            'name': 'Test',
            'surname': 'User',
            'patronymic': 'Patronymic',
            'birthday': '1990-01-01',
            'password': 'password123',
        }

    def tearDown(self):
        get_user_model().objects.all().delete()

    def test_create_patient_user(self):
        user_data = self.user_data
        user_data.update(self.patient_data)
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        user = serializer.save()
        self.assertEqual(self.user_data['email'], str(user))

    def test_create_doctor_user(self):
        user_data = self.user_data
        user_data.update(self.doctor_data)
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        user = serializer.save()
        self.assertEqual(self.user_data['email'], str(user))

    def test_create_manager_user(self):
        user_data = self.user_data
        user_data.update(self.manager_data)
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        user = serializer.save()
        self.assertEqual(self.user_data['email'], str(user))

    def test_invalid_data(self):
        with self.assertRaises(ValidationError):
            serializer = UserSerializer(data={})
            serializer.is_valid(raise_exception=True)


class AuthTest(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.test_user_data = {
            'name': 'Test',
            'surname': 'User',
            'patronymic': 'Patronymic',
            'birthday': '1990-01-01',
            'password': 'password12345',
            'email': 'testuser@test.com',
            'phone': '+79001234555',
        }
        cls.user = get_user_model().objects.create_user(**cls.test_user_data)

    def test_registration(self):
        user_data = {
            'name': 'Test',
            'surname': 'User',
            'patronymic': 'Patronymic',
            'birthday': '1990-01-01',
            'password': 'password123',
            'patient': {'role': 'patient'},
            'email': 'testuser@example.com',
            'phone': '+79001234568',
        }
        view = RegistrationAPIView().as_view()
        request = self.factory.post(reverse('registration'), data=user_data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_login_logout(self):
        login_view = LoginAPIView().as_view()
        request = self.factory.post(reverse('login'), data={'email': self.test_user_data['email'],
                                                            'password': self.test_user_data['password']}, format='json')
        response = login_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request = self.factory.post(reverse('logout'), data={'refresh_token': response.data['refresh']}, format='json')
        logout_view = LogoutAPIView().as_view()
        response = logout_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
